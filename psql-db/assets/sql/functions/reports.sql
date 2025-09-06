/* DAILY SUMMARY */
CREATE OR REPLACE FUNCTION get_daily_summary(p_date DATE)
RETURNS TABLE (
    total_hospitalizations INTEGER,
    total_surgeries INTEGER,
    total_prescriptions INTEGER,
    total_amount_spent NUMERIC
) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        CAST(COUNT(DISTINCT h.id) AS INTEGER) AS total_hospitalizations,
        CAST(COUNT(DISTINCT s.id) AS INTEGER) AS total_surgeries,
        CAST(COUNT(DISTINCT p.id) AS INTEGER) AS total_prescriptions,
        COALESCE(CAST(SUM(pm.amount) AS NUMERIC), 0) AS total_amount_spent
    FROM 
        hospitalization h
    LEFT JOIN 
        surgery s ON h.id = s.hospitalization_id AND DATE(s.clinical_date) = p_date
    LEFT JOIN 
        hospitalization_prescription hp ON h.id = hp.hospitalization_id
    LEFT JOIN 
        prescription p ON hp.prescription_id = p.id AND DATE(p.validity) = p_date
    LEFT JOIN 
        payment pm ON DATE(pm.payment_time) = p_date AND pm.patient_id = h.patient_id
    WHERE 
        DATE(h.start_date) = p_date;
END;
$$ LANGUAGE plpgsql;

/* MONTHLY REPORT */
CREATE OR REPLACE FUNCTION get_monthly_report()
RETURNS TABLE (
    month TEXT,
    doctor TEXT,
    total_surgeries INTEGER
) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        to_char(s.clinical_date, 'YYYY-MM') AS month,
        CAST(d.name AS TEXT) AS doctor,
        CAST(COUNT(s.id) AS INTEGER) AS total_surgeries
    FROM 
        surgery s
    JOIN 
        doctor d ON s.doctor_id = d.id
    WHERE 
        s.clinical_date >= (CURRENT_DATE - INTERVAL '12 months')
    GROUP BY 
        month, d.name
    ORDER BY 
        month DESC, total_surgeries DESC;
END;
$$ LANGUAGE plpgsql;

/* TOP 3*/
CREATE OR REPLACE FUNCTION top3()
RETURNS TABLE(
    patient_name VARCHAR,
    amount_spent NUMERIC,
    procedure_id BIGINT,
    doctor_id BIGINT,
    procedure_date TIMESTAMP,
    cost NUMERIC,
    procedure_type VARCHAR
) 
LANGUAGE plpgsql
AS $$
BEGIN
    RETURN QUERY
    WITH patient_spending AS (
        SELECT 
            p.id AS patient_id,
            p.name AS patient_name,
            CAST(SUM(pay.amount) AS NUMERIC) AS amount_spent
        FROM 
            patient p
        JOIN 
            bill b ON p.id = b.patient_id
        JOIN 
            payment pay ON b.id = pay.bill_id
        WHERE 
            DATE_TRUNC('month', pay.payment_time) = DATE_TRUNC('month', CURRENT_DATE)
        GROUP BY 
            p.id, p.name
        ORDER BY 
            SUM(pay.amount) DESC
        LIMIT 3
    ),
    procedures AS (
        SELECT 
            a.id AS procedure_id,
            a.patient_id,
            a.doctor_id,
            a.clinical_date AS procedure_date,
            CAST(a.cost AS NUMERIC) AS cost,
            CAST('appointment' AS VARCHAR) AS procedure_type
        FROM 
            appointment a
        WHERE 
            DATE_TRUNC('month', a.clinical_date) = DATE_TRUNC('month', CURRENT_DATE)
        
        UNION ALL
        
        SELECT 
            s.id AS procedure_id,
            s.patient_id,
            s.doctor_id,
            s.clinical_date AS procedure_date,
            CAST(s.cost AS NUMERIC) AS cost,
            CAST('surgery' AS VARCHAR) AS procedure_type
        FROM 
            surgery s
        WHERE 
            DATE_TRUNC('month', s.clinical_date) = DATE_TRUNC('month', CURRENT_DATE)
    )
    SELECT 
        ps.patient_name,
        ps.amount_spent,
        proc.procedure_id,
        proc.doctor_id,
        proc.procedure_date,
        proc.cost,
        proc.procedure_type
    FROM 
        patient_spending ps
    JOIN 
        procedures proc ON ps.patient_id = proc.patient_id
    ORDER BY 
        ps.amount_spent DESC, proc.procedure_date DESC;
END;
$$;
/* functions */

/*LOGIN*/
CREATE OR REPLACE FUNCTION verify_login(p_username TEXT, p_password TEXT)
RETURNS TABLE(user_id BIGINT, username TEXT, user_type TEXT, password TEXT) AS $$
BEGIN
    RETURN QUERY
    SELECT id, CAST(patient.username AS TEXT), 'patient' as user_type, CAST(patient.password AS TEXT)
    FROM patient
    WHERE patient.username = p_username
    UNION ALL
    SELECT id, CAST(doctor.username AS TEXT), 'doctor' as user_type, CAST(doctor.password AS TEXT)
    FROM doctor
    WHERE doctor.username = p_username
    UNION ALL
    SELECT id, CAST(nurse.username AS TEXT), 'nurse' as user_type, CAST(nurse.password AS TEXT)
    FROM nurse
    WHERE nurse.username = p_username
    UNION ALL
    SELECT id, CAST(assistant.username AS TEXT), 'assistant' as user_type, CAST(assistant.password AS TEXT)
    FROM assistant
    WHERE assistant.username = p_username;
END;
$$ LANGUAGE plpgsql;


/*REGIST */

CREATE OR REPLACE FUNCTION insert_patient(
    p_name TEXT, p_email TEXT, p_phone BIGINT, p_username TEXT, p_password TEXT
) RETURNS BIGINT AS $$
DECLARE
    v_user_id BIGINT;
BEGIN
    INSERT INTO patient (name, email, phone, username, password)
    VALUES (p_name, p_email, p_phone, p_username, p_password)
    RETURNING id INTO v_user_id;
    RETURN v_user_id;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION insert_assistant(
    p_start_date DATE, p_due_date DATE, p_salary INTEGER, p_name TEXT, p_email TEXT, p_phone BIGINT, p_username TEXT, p_password TEXT
) RETURNS BIGINT AS $$
DECLARE
    v_user_id BIGINT;
BEGIN
    INSERT INTO assistant (start_date, due_date, salary, name, email, phone, username, password)
    VALUES (p_start_date, p_due_date, p_salary, p_name, p_email, p_phone, p_username, p_password)
    RETURNING id INTO v_user_id;
    RETURN v_user_id;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION insert_nurse(
    p_hierarchy INTEGER, p_start_date DATE, p_due_date DATE, p_salary INTEGER, p_name TEXT, p_email TEXT, p_phone BIGINT, p_username TEXT, p_password TEXT
) RETURNS BIGINT AS $$
DECLARE
    v_user_id BIGINT;
BEGIN
    INSERT INTO nurse (hierarchy, start_date, due_date, salary, name, email, phone, username, password)
    VALUES (p_hierarchy, p_start_date, p_due_date, p_salary, p_name, p_email, p_phone, p_username, p_password)
    RETURNING id INTO v_user_id;
    RETURN v_user_id;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION insert_doctor(
    p_license TEXT, p_start_date DATE, p_due_date DATE, p_salary INTEGER, p_name TEXT, p_email TEXT, p_phone BIGINT, p_username TEXT, p_password TEXT
) RETURNS BIGINT AS $$
DECLARE
    v_user_id BIGINT;
BEGIN
    INSERT INTO doctor (license, start_date, due_date, salary, name, email, phone, username, password)
    VALUES (p_license, p_start_date, p_due_date, p_salary, p_name, p_email, p_phone, p_username, p_password)
    RETURNING id INTO v_user_id;
    RETURN v_user_id;
END;
$$ LANGUAGE plpgsql;



/* GET APPOINTMENTS*/
CREATE OR REPLACE FUNCTION get_patient_appointments(p_patient_id BIGINT)
RETURNS TABLE (
    appointment_id BIGINT,
    doctor_id BIGINT,
    clinical_date TIMESTAMP,
    doctor_name TEXT
) AS $$
BEGIN
    RETURN QUERY
    SELECT a.id AS appointment_id, a.doctor_id, a.clinical_date, CAST(d.name AS TEXT) AS doctor_name
    FROM appointment a
    JOIN doctor d ON a.doctor_id = d.id
    WHERE a.patient_id = p_patient_id;
END;
$$ LANGUAGE plpgsql;


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




/* SCHEDULE SURGERY*/
CREATE OR REPLACE FUNCTION schedule_surgery_fn(
    p_patient_id BIGINT,
    p_doctor_id BIGINT,
    p_nurse_ids BIGINT[],
    p_roles TEXT[],
    p_clinical_date TIMESTAMP,
    p_surgery_duration BIGINT,
    p_surgery_cost FLOAT,
    p_hospitalization_id BIGINT DEFAULT NULL
) RETURNS TABLE (
    hospitalization_id BIGINT,
    surgery_id BIGINT,
    surgery_bill_id BIGINT
) AS $$
DECLARE
    first_nurse_id BIGINT;
    new_hospitalization_id BIGINT;
BEGIN
    IF p_hospitalization_id IS NULL THEN
        IF array_length(p_nurse_ids, 1) IS NULL OR array_length(p_nurse_ids, 1) = 0 THEN
            RAISE EXCEPTION 'Nurses list cannot be empty when creating a new hospitalization';
        END IF;

        first_nurse_id := p_nurse_ids[1];

        INSERT INTO hospitalization (duration, start_date, bill_id, patient_id, nurse_id)
        VALUES (p_surgery_duration, p_clinical_date, NULL, p_patient_id, first_nurse_id)
        RETURNING id INTO new_hospitalization_id;
    ELSE
        new_hospitalization_id := p_hospitalization_id;
    END IF;

    INSERT INTO surgery (hospitalization_id, cost, duration, clinical_date, bill_id, patient_id, doctor_id)
    VALUES (new_hospitalization_id, p_surgery_cost, p_surgery_duration, p_clinical_date, NULL, p_patient_id, p_doctor_id)
    RETURNING surgery.id, surgery.bill_id INTO surgery_id, surgery_bill_id;

    FOR i IN 1..array_length(p_nurse_ids, 1) LOOP
        INSERT INTO functionalities (functionality, surgery_id, nurse_id)
        VALUES (p_roles[i], surgery_id, p_nurse_ids[i]);
    END LOOP;

    RETURN QUERY SELECT new_hospitalization_id, surgery_id, surgery_bill_id;
END;
$$ LANGUAGE plpgsql;


/* REPORT*/
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



/* EXECUTE PAYMENT*/
CREATE OR REPLACE FUNCTION process_payment(
    p_bill_id BIGINT,
    p_patient_id BIGINT,
    p_amount NUMERIC,
    p_payment_method TEXT
)
RETURNS TABLE (
    remaining_value NUMERIC
) AS $$
DECLARE
    bill_total_cost NUMERIC;
BEGIN
    -- Verificar se a fatura pertence ao paciente autenticado e obter o valor total atual da fatura
    IF NOT EXISTS (SELECT 1 FROM bill WHERE id = p_bill_id AND patient_id = p_patient_id) THEN
        RAISE EXCEPTION 'Bill not found or does not belong to the patient';
    END IF;

    -- Obter o valor total da fatura
    SELECT total_cost INTO bill_total_cost FROM bill WHERE id = p_bill_id;

    -- Verificar se a fatura já está paga ou se o valor do pagamento excede o valor restante
    IF bill_total_cost <= 0 THEN
        RAISE EXCEPTION 'This bill is already fully paid and cannot accept further payments';
    ELSIF p_amount > bill_total_cost THEN
        RAISE EXCEPTION 'Payment amount exceeds the remaining value of the bill';
    END IF;

    -- Inserir o pagamento na tabela payment
    INSERT INTO payment (amount, payment_time, patient_id, bill_id, method)
    VALUES (p_amount, CURRENT_DATE, p_patient_id, p_bill_id, p_payment_method);

    -- Atualizar o valor total da fatura
    UPDATE bill
    SET total_cost = bill_total_cost - p_amount
    WHERE id = p_bill_id;

    -- Obter o valor restante atualizado
    SELECT total_cost INTO remaining_value FROM bill WHERE id = p_bill_id;

    RETURN QUERY SELECT remaining_value;
END;
$$ LANGUAGE plpgsql;


/* ADD PRESCRIPTION*/
CREATE OR REPLACE FUNCTION add_prescription(
    p_type TEXT,
    p_event_id BIGINT,
    p_validity DATE,
    p_medicines JSONB
)
RETURNS TABLE (
    prescription_id BIGINT
) AS $$
DECLARE
    new_prescription_id BIGINT;
    medicine_id BIGINT;
    medicine JSONB;
    med_name TEXT;
    med_composition TEXT;
    med_period INT;
    med_amount TEXT;
BEGIN
    -- Inserir a nova prescrição
    INSERT INTO prescription (validity)
    VALUES (p_validity)
    RETURNING id INTO new_prescription_id;

    -- Associar a prescrição ao evento
    IF p_type = 'hospitalization' THEN
        -- Verificar se já existe uma prescrição para esta hospitalização
        IF EXISTS (SELECT 1 FROM hospitalization_prescription WHERE hospitalization_id = p_event_id) THEN
            RAISE EXCEPTION 'Prescription already exists for this hospitalization';
        END IF;
        INSERT INTO hospitalization_prescription (hospitalization_id, prescription_id)
        VALUES (p_event_id, new_prescription_id);
    ELSIF p_type = 'appointment' THEN
        -- Verificar se já existe uma prescrição para esta consulta
        IF EXISTS (SELECT 1 FROM appointment_prescription WHERE appointment_id = p_event_id) THEN
            RAISE EXCEPTION 'Prescription already exists for this appointment';
        END IF;
        INSERT INTO appointment_prescription (appointment_id, prescription_id)
        VALUES (p_event_id, new_prescription_id);
    ELSE
        RAISE EXCEPTION 'Invalid prescription type';
    END IF;

    -- Preparar os dados dos medicamentos
    FOR medicine IN SELECT * FROM jsonb_array_elements(p_medicines) LOOP
        med_name := medicine->>'medicine';
        med_composition := COALESCE(medicine->>'composition', '');
        med_period := (medicine->>'period')::INT;
        med_amount := medicine->>'amount';

        INSERT INTO medicine (name, composition)
        VALUES (med_name, med_composition)
        ON CONFLICT (name) DO NOTHING
        RETURNING id INTO medicine_id;

        IF medicine_id IS NULL THEN
            SELECT id INTO medicine_id FROM medicine WHERE name = med_name;
        END IF;

        INSERT INTO dosage (period, amount, medicine_id, prescription_id)
        VALUES (med_period, med_amount, medicine_id, new_prescription_id);
    END LOOP;

    RETURN QUERY SELECT new_prescription_id;
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

/* SCHEDULE APPOINTMENT */

CREATE OR REPLACE FUNCTION create_appointment(
    p_patient_id BIGINT,
    p_doctor_id BIGINT,
    p_date TIMESTAMP,
    p_duration BIGINT,
    p_cost NUMERIC
)
RETURNS BIGINT
LANGUAGE plpgsql
AS $$
DECLARE
    v_appointment_id BIGINT;
BEGIN
    INSERT INTO appointment (patient_id, doctor_id, clinical_date, duration, cost)
    VALUES (p_patient_id, p_doctor_id, p_date, p_duration, p_cost)
    RETURNING id INTO v_appointment_id;
    RETURN v_appointment_id;
END;
$$;


/* GET PRESCRIPTIONS */

CREATE OR REPLACE FUNCTION get_prescriptions_for_patient(p_patient_id BIGINT)
RETURNS TABLE (
    prescription_id BIGINT,
    validity DATE,
    posology JSONB
) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        pr.id AS prescription_id,
        pr.validity,
        jsonb_agg(jsonb_build_object(
            'dose', d.amount,
            'frequency', d.period,
            'medicine', m.name
        )) AS posology
    FROM prescription pr
    LEFT JOIN dosage d ON pr.id = d.prescription_id
    LEFT JOIN medicine m ON d.medicine_id = m.id
    LEFT JOIN hospitalization_prescription hp ON pr.id = hp.prescription_id
    LEFT JOIN hospitalization h ON hp.hospitalization_id = h.id
    LEFT JOIN appointment_prescription ap ON pr.id = ap.prescription_id
    LEFT JOIN appointment a ON ap.appointment_id = a.id
    WHERE h.patient_id = p_patient_id OR a.patient_id = p_patient_id
    GROUP BY pr.id;
END;
$$ LANGUAGE plpgsql;
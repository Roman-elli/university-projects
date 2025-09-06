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
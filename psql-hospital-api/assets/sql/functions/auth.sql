/* LOGIN */
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


/* REGISTER */
/* PATIENT */
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

/* ASSISTANT */
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

/* NURSE */
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

/* DOCTOR */
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
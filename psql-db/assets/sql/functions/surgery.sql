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
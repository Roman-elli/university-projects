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
    INSERT INTO prescription (validity)
    VALUES (p_validity)
    RETURNING id INTO new_prescription_id;

    IF p_type = 'hospitalization' THEN
        IF EXISTS (SELECT 1 FROM hospitalization_prescription WHERE hospitalization_id = p_event_id) THEN
            RAISE EXCEPTION 'Prescription already exists for this hospitalization';
        END IF;
        INSERT INTO hospitalization_prescription (hospitalization_id, prescription_id)
        VALUES (p_event_id, new_prescription_id);
    ELSIF p_type = 'appointment' THEN
        IF EXISTS (SELECT 1 FROM appointment_prescription WHERE appointment_id = p_event_id) THEN
            RAISE EXCEPTION 'Prescription already exists for this appointment';
        END IF;
        INSERT INTO appointment_prescription (appointment_id, prescription_id)
        VALUES (p_event_id, new_prescription_id);
    ELSE
        RAISE EXCEPTION 'Invalid prescription type';
    END IF;

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
CREATE OR REPLACE FUNCTION create_bill_for_appointment()
RETURNS TRIGGER
LANGUAGE plpgsql
AS $$
DECLARE
    v_bill_id BIGINT;
BEGIN
    INSERT INTO bill (total_cost, type, patient_id)
    VALUES (NEW.cost, false, NEW.patient_id)
    RETURNING id INTO v_bill_id;

    NEW.bill_id = v_bill_id;

    RETURN NEW;
END;
$$;

CREATE TRIGGER trigger_create_bill
BEFORE INSERT ON appointment
FOR EACH ROW
EXECUTE FUNCTION create_bill_for_appointment();
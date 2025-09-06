CREATE OR REPLACE FUNCTION create_or_update_bill() RETURNS TRIGGER AS $$
DECLARE
    existing_bill_id BIGINT;
BEGIN
    IF NEW.hospitalization_id IS NOT NULL THEN
        SELECT bill_id INTO existing_bill_id FROM hospitalization WHERE id = NEW.hospitalization_id;

        IF existing_bill_id IS NOT NULL THEN
            UPDATE bill SET total_cost = total_cost + NEW.cost WHERE id = existing_bill_id;
            NEW.bill_id = existing_bill_id;
        ELSE
            INSERT INTO bill (total_cost, type, patient_id) VALUES (NEW.cost, TRUE, NEW.patient_id) RETURNING id INTO NEW.bill_id;
            UPDATE hospitalization SET bill_id = NEW.bill_id WHERE id = NEW.hospitalization_id;
        END IF;
    ELSE
        INSERT INTO bill (total_cost, type, patient_id) VALUES (NEW.cost, TRUE, NEW.patient_id) RETURNING id INTO NEW.bill_id;
    END IF;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trigger_create_or_update_bill
BEFORE INSERT ON surgery
FOR EACH ROW
EXECUTE PROCEDURE create_or_update_bill();

CREATE OR REPLACE FUNCTION update_bill_id() RETURNS TRIGGER AS $$
BEGIN
    IF NEW.hospitalization_id IS NOT NULL THEN
        UPDATE hospitalization SET bill_id = NEW.bill_id WHERE id = NEW.hospitalization_id;
    END IF;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trigger_update_bill_id
AFTER INSERT ON surgery
FOR EACH ROW
EXECUTE PROCEDURE update_bill_id();
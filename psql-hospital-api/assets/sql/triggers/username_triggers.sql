CREATE OR REPLACE FUNCTION check_unique_username() RETURNS TRIGGER AS $$
BEGIN
    IF EXISTS (SELECT 1 FROM patient WHERE username = NEW.username) OR
       EXISTS (SELECT 1 FROM doctor WHERE username = NEW.username) OR
       EXISTS (SELECT 1 FROM nurse WHERE username = NEW.username) OR
       EXISTS (SELECT 1 FROM assistant WHERE username = NEW.username) THEN
        RAISE EXCEPTION 'Username already exists';
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER patient_check_unique_username
BEFORE INSERT ON patient
FOR EACH ROW
EXECUTE FUNCTION check_unique_username();

CREATE TRIGGER doctor_check_unique_username
BEFORE INSERT ON doctor
FOR EACH ROW
EXECUTE FUNCTION check_unique_username();

CREATE TRIGGER nurse_check_unique_username
BEFORE INSERT ON nurse
FOR EACH ROW
EXECUTE FUNCTION check_unique_username();

CREATE TRIGGER assistant_check_unique_username
BEFORE INSERT ON assistant
FOR EACH ROW
EXECUTE FUNCTION check_unique_username();

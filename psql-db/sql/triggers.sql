/* CHECK BILL */
-- Função para criar ou atualizar a fatura antes da cirurgia
CREATE OR REPLACE FUNCTION create_or_update_bill() RETURNS TRIGGER AS $$
DECLARE
    existing_bill_id BIGINT;
BEGIN
    IF NEW.hospitalization_id IS NOT NULL THEN
        -- Buscar o bill_id da hospitalização existente
        SELECT bill_id INTO existing_bill_id FROM hospitalization WHERE id = NEW.hospitalization_id;
        -- Verificar se a hospitalização já possui uma fatura associada
        IF existing_bill_id IS NOT NULL THEN
            -- Atualizar a fatura existente associada à hospitalização
            UPDATE bill SET total_cost = total_cost + NEW.cost WHERE id = existing_bill_id;
            NEW.bill_id = existing_bill_id;
        ELSE
            -- Criar uma nova fatura
            INSERT INTO bill (total_cost, type, patient_id) VALUES (NEW.cost, TRUE, NEW.patient_id) RETURNING id INTO NEW.bill_id;
            -- Atualizar a hospitalização para associar a nova fatura
            UPDATE hospitalization SET bill_id = NEW.bill_id WHERE id = NEW.hospitalization_id;
        END IF;
    ELSE
        -- Criar uma nova fatura
        INSERT INTO bill (total_cost, type, patient_id) VALUES (NEW.cost, TRUE, NEW.patient_id) RETURNING id INTO NEW.bill_id;
    END IF;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Gatilho para criar ou atualizar a fatura antes da inserção de uma cirurgia
CREATE TRIGGER trigger_create_or_update_bill
BEFORE INSERT ON surgery
FOR EACH ROW
EXECUTE PROCEDURE create_or_update_bill();



-- Função para atualizar o bill_id em surgery e hospitalization após inserção
CREATE OR REPLACE FUNCTION update_bill_id() RETURNS TRIGGER AS $$
BEGIN
    IF NEW.hospitalization_id IS NOT NULL THEN
        -- Atualizar o bill_id na hospitalização
        UPDATE hospitalization SET bill_id = NEW.bill_id WHERE id = NEW.hospitalization_id;
    END IF;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Gatilho para atualizar o bill_id após a inserção de uma cirurgia
CREATE TRIGGER trigger_update_bill_id
AFTER INSERT ON surgery
FOR EACH ROW
EXECUTE PROCEDURE update_bill_id();


/* CHECK USERNAME */
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


-- Gatilho para a tabela patient
CREATE TRIGGER patient_check_unique_username
BEFORE INSERT ON patient
FOR EACH ROW
EXECUTE FUNCTION check_unique_username();

-- Gatilho para a tabela doctor
CREATE TRIGGER doctor_check_unique_username
BEFORE INSERT ON doctor
FOR EACH ROW
EXECUTE FUNCTION check_unique_username();

-- Gatilho para a tabela nurse
CREATE TRIGGER nurse_check_unique_username
BEFORE INSERT ON nurse
FOR EACH ROW
EXECUTE FUNCTION check_unique_username();

-- Gatilho para a tabela assistant
CREATE TRIGGER assistant_check_unique_username
BEFORE INSERT ON assistant
FOR EACH ROW
EXECUTE FUNCTION check_unique_username();


-- Criar bill referente ao appointment gerado
CREATE OR REPLACE FUNCTION create_bill_for_appointment()
RETURNS TRIGGER
LANGUAGE plpgsql
AS $$
DECLARE
    v_bill_id BIGINT;
BEGIN
    -- Insert the new bill
    INSERT INTO bill (total_cost, type, patient_id)
    VALUES (NEW.cost, false, NEW.patient_id)
    RETURNING id INTO v_bill_id;

    -- Update the new appointment with the bill ID
    NEW.bill_id = v_bill_id;

    RETURN NEW;
END;
$$;

CREATE TRIGGER trigger_create_bill
BEFORE INSERT ON appointment
FOR EACH ROW
EXECUTE FUNCTION create_bill_for_appointment();
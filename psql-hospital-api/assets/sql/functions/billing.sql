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
    IF NOT EXISTS (SELECT 1 FROM bill WHERE id = p_bill_id AND patient_id = p_patient_id) THEN
        RAISE EXCEPTION 'Bill not found or does not belong to the patient';
    END IF;

    SELECT total_cost INTO bill_total_cost FROM bill WHERE id = p_bill_id;

    IF bill_total_cost <= 0 THEN
        RAISE EXCEPTION 'This bill is already fully paid and cannot accept further payments';
    ELSIF p_amount > bill_total_cost THEN
        RAISE EXCEPTION 'Payment amount exceeds the remaining value of the bill';
    END IF;

    INSERT INTO payment (amount, payment_time, patient_id, bill_id, method)
    VALUES (p_amount, CURRENT_DATE, p_patient_id, p_bill_id, p_payment_method);

    UPDATE bill
    SET total_cost = bill_total_cost - p_amount
    WHERE id = p_bill_id;

    SELECT total_cost INTO remaining_value FROM bill WHERE id = p_bill_id;

    RETURN QUERY SELECT remaining_value;
END;
$$ LANGUAGE plpgsql;

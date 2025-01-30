CREATE OR REPLACE FUNCTION get_claims_by_patient(patient_id_param INT)
RETURNS TABLE (claim_id VARCHAR, claim_amount DECIMAL, patient_id INT) AS $$
BEGIN
    RETURN QUERY
    SELECT c.claim_id, c.claim_amount, c.patient_id
    FROM claims c
    WHERE c.patient_id = patient_id_param;
END;
$$ LANGUAGE plpgsql;



CREATE OR REPLACE FUNCTION get_monthly_claims()
RETURNS TABLE (month TEXT, total_claims INT) AS $$
BEGIN
    RETURN QUERY
    SELECT TO_CHAR(transaction_date, 'YYYY-MM') AS month, COUNT(*) AS total_claims
    FROM transactions
    GROUP BY month
    ORDER BY month DESC;
END;
$$ LANGUAGE plpgsql;


CREATE OR REPLACE FUNCTION get_top_claims(n INT)
RETURNS TABLE (claim_id VARCHAR, claim_amount DECIMAL) AS $$
BEGIN
    RETURN QUERY
    SELECT claim_id, claim_amount
    FROM claims
    ORDER BY claim_amount DESC
    LIMIT n;
END;
$$ LANGUAGE plpgsql;


CREATE OR REPLACE FUNCTION get_frequent_claim_patients(n INT)
RETURNS TABLE (first_name VARCHAR, last_name VARCHAR, claim_count INT) AS $$
BEGIN
    RETURN QUERY
    SELECT p.first_name, p.last_name, COUNT(c.id) AS claim_count
    FROM claims c
    JOIN patients p ON c.patient_id = p.id
    GROUP BY p.first_name, p.last_name
    HAVING COUNT(c.id) > n
    ORDER BY claim_count DESC;
END;
$$ LANGUAGE plpgsql;

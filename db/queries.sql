SELECT p.first_name, p.last_name, SUM(c.claim_amount) AS total_claims
FROM claims c
JOIN patients p ON c.patient_id = p.id
GROUP BY p.first_name, p.last_name
ORDER BY total_claims DESC;



SELECT edi_filename, sender_id, receiver_id, transaction_date
FROM transactions
ORDER BY transaction_date DESC
LIMIT 10;


SELECT claim_id, claim_amount
FROM claims
ORDER BY claim_amount DESC
LIMIT 5;


SELECT p.first_name, p.last_name, COUNT(c.id) AS claim_count
FROM claims c
JOIN patients p ON c.patient_id = p.id
GROUP BY p.first_name, p.last_name
ORDER BY claim_count DESC;

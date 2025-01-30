import psycopg2
import os
from parse_edi import parse_edi_file


DB_CONFIG = {
  "dbname": "edi_development_database",
  "user": "edi_user",
  "password": "edi_dev",
  "host": "localhost",
  "port": "5432"
}

def connect_db():
    """Establish connection to PostgreSQL and confirm connection success."""
    try:
        print("Attempting to connect to the database...")
        conn = psycopg2.connect(**DB_CONFIG)
        print("✅ Successfully connected to the database!")
        return conn
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        return None


def insert_patient(cursor, first_name, last_name, member_id):
    """Insert a patient into the database if they don’t exist."""
    cursor.execute("""
        INSERT INTO patients (first_name, last_name, member_id)
        VALUES (%s, %s, %s)
        ON CONFLICT (member_id) DO NOTHING
        RETURNING id;
    """, (first_name, last_name, member_id))

    result = cursor.fetchone()
    return result[0] if result else None  # Return patient ID if inserted


def insert_claim(cursor, claim_id, claim_amount, patient_id):
    """Insert a claim into the database."""
    cursor.execute("""
        INSERT INTO claims (claim_id, claim_amount, patient_id)
        VALUES (%s, %s, %s)
        ON CONFLICT (claim_id) DO NOTHING;
    """, (claim_id, claim_amount, patient_id))


def insert_transaction(cursor, edi_filename, sender_id, receiver_id, transaction_date):
    """Insert EDI transaction metadata into the transactions table."""
    cursor.execute("""
        INSERT INTO transactions (edi_filename, sender_id, receiver_id, transaction_date)
        VALUES (%s, %s, %s, %s);
    """, (edi_filename, sender_id, receiver_id, transaction_date))


def transform_and_store_data(edi_file):
    """Parses EDI data, transforms it, and stores it in the database."""
    if not os.path.exists(edi_file):
        print(f"Error: File {edi_file} not found")
        return

    parsed_data = parse_edi_file(edi_file)

    with connect_db() as conn:
        with conn.cursor() as cursor:
            # Insert transaction metadata
            insert_transaction(cursor, edi_file, parsed_data["Sender ID"], parsed_data["Receiver ID"], parsed_data["Date"])

            for patient in parsed_data["Patient Names"]:
                first_name, last_name = patient.split(" ")
                patient_id = insert_patient(cursor, first_name, last_name, "123456789")  # Dummy member ID for now

                for claim in parsed_data["Claims"]:
                    insert_claim(cursor, claim["Claim ID"], claim["Claim Amount"], patient_id)

            conn.commit()

if __name__ == "__main__":
    edi_file = "../data/raw_data/claims_837.edi"
    transform_and_store_data(edi_file)
    print("✅ Data transformation and storage completed!")
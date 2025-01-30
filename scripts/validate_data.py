import re
import os
from parse_edi import parse_edi_file

def validate_edi_data(parsed_data):
    """
    Validates extracted EDI data for required fields, formatting, and completeness.
    """

    errors = []

    # Validate Sender & Receiver IDs
    if not parsed_data["Sender ID"] or not re.match(r"^[A-Z0-9]+$", parsed_data["Sender ID"]):
        errors.append("Invalid or missing Sender ID")
    if not parsed_data["Receiver ID"] or not re.match(r"^[A-Z0-9]+$", parsed_data["Receiver ID"]):
        errors.append("Invalid or missing Receiver ID")

    # Validate Date (Should be in YYMMDD format)
    if not parsed_data["Date"] or not re.match(r"^\d{6}$", parsed_data["Date"]):
        errors.append("Invalid or missing transaction date")

    # Validate Claims
    for claim in parsed_data["Claims"]:
        if not claim["Claim ID"] or not re.match(r"^\d+$", claim["Claim ID"]):
            errors.append(f"Invalid Claim ID: {claim['Claim ID']}")
        if not claim["Claim Amount"] or not re.match(r"^\d+(\.\d{2})?$", claim["Claim Amount"]):
            errors.append(f"Invalid Claim Amount: {claim['Claim Amount']}")

    # Validate Patient Names
    if not parsed_data["Patient Names"]:
        errors.append("No patient names found in EDI file")

    return errors

if __name__ == "__main__":
    edi_file = "../data/raw_data/claims_837.edi"

    if not os.path.exists(edi_file):
        print(f"Error: File {edi_file} not found")
    else:
        parsed_output = parse_edi_file(edi_file)
        validation_errors = validate_edi_data(parsed_output)

        if validation_errors:
            print("\n⚠️ Validation Errors Found:")
            for error in validation_errors:
                print(f"- {error}")
        else:
            print("\n✅ No validation errors. EDI data is valid!")

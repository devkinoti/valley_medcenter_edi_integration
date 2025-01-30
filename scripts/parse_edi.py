import os

def parse_edi_file(file_path):
    """
    Parses an X12 EDI file and extracts key segments
    """

    if not os.path.exists(file_path):
        print(f"Error: File {file_path} not found")
        return

    with open(file_path, "r", encoding="utf-8") as file:
        edi_content = file.read().strip()

    segments = edi_content.split("~")

    print("\n--- DEBUG: Printing First 10 Segments ---")
    for i, segment in enumerate(segments[:10]):  # Print first 10 segments for debugging
        print(f"{i+1}: {segment}")

    parsed_data = {
        "Sender ID": "",
        "Receiver ID": "",
        "Date": "",
        "Time": "",
        "Patient Names": [],
        "Claims": [],
        "Eligibility Requests": []
    }

    for segment in segments:
        elements = segment.strip().split("*")  # Trim spaces
        segment_type = elements[0].strip() if elements else ""

        if segment_type == "ISA":
            parsed_data["Sender ID"] = elements[6].strip() if len(elements) > 6 else ""
            parsed_data["Receiver ID"] = elements[8].strip() if len(elements) > 8 else ""
            parsed_data["Date"] = elements[9].strip() if len(elements) > 9 else ""
            parsed_data["Time"] = elements[10].strip() if len(elements) > 10 else ""

        elif segment_type == "NM1" and len(elements) > 3 and elements[1] == "IL":
            # Debugging statement
            print(f"DEBUG: Found NM1 - {elements}")
            first_name = elements[3].strip() if len(elements) > 3 else "UNKNOWN"
            last_name = elements[4].strip() if len(elements) > 4 else "UNKNOWN"
            patient_name = f"{first_name} {last_name}"
            parsed_data["Patient Names"].append(patient_name)

        elif segment_type == "CLM":
            print(f"DEBUG: Found CLM - {elements}")
            claim_id = elements[1].strip() if len(elements) > 1 else "UNKNOWN"
            claim_amount = elements[2].strip() if len(elements) > 2 else "0.00"
            parsed_data["Claims"].append({"Claim ID": claim_id, "Claim Amount": claim_amount})

        elif segment_type == "EQ":
            print(f"DEBUG: Found EQ - {elements}")
            eligibility_request = elements[1].strip() if len(elements) > 1 else "UNKNOWN"
            parsed_data["Eligibility Requests"].append(eligibility_request)

    return parsed_data

if __name__ == "__main__":
    edi_file = "../data/raw_data/claims_837.edi"
    parsed_output = parse_edi_file(edi_file)
    if parsed_output:
        print("\nParsed EDI Data:")
        for key, value in parsed_output.items():
            print(f"{key}: {value}")

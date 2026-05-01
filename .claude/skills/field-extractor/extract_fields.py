import sys
import json
# Example logic using a hypothetical library
def extract_pdf_data(filepath):
    # Deterministic code to parse the PDF
    return {"invoice_id": "INV-123", "total": 150.00}

if __name__ == "__main__":
    result = extract_pdf_data(sys.argv[1])
    print(json.dumps(result))

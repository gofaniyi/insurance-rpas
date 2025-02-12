
import csv
import re
import pdfplumber

INVOICE_FILE = "sample_invoice.pdf"
OUTPUT_FILE = "invoice_data.csv"


def extract_invoice_data():
    with pdfplumber.open(INVOICE_FILE) as pdf:
        text = "\n".join(page.extract_text()
                         for page in pdf.pages if page.extract_text())

    invoices = re.findall(
        r"Invoice No: (\d+).*?Total: \$(\d+\.\d{2})", text, re.DOTALL)

    with open(OUTPUT_FILE, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Invoice No", "Total Amount"])

        for invoice_no, total_amount in invoices:
            writer.writerow([invoice_no, total_amount])

    print(f"Extracted invoice data saved to {OUTPUT_FILE}")


if __name__ == "__main__":
    extract_invoice_data()

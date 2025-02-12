import imaplib
import email
import fitz  # PyMuPDF
import pytesseract
import requests
import os
from email.header import decode_header
from email.utils import parsedate_to_datetime

# Email Configuration
IMAP_SERVER = "<EMAIL_SERVER>"  # Change to your email provider's IMAP server
EMAIL_USER = "<EMAIL_USER>"
EMAIL_PASS = "<EMAIL_PASS>"
CLAIM_API_URL = "<CLAIM_API_URL>"  # Example API

# Connect to Email Inbox


def fetch_unread_emails():
    try:
        mail = imaplib.IMAP4_SSL(IMAP_SERVER)
        mail.login(EMAIL_USER, EMAIL_PASS)
        mail.select("inbox")

        status, messages = mail.search(None, "UNSEEN")
        email_ids = messages[0].split()

        for email_id in email_ids:
            status, msg_data = mail.fetch(email_id, "(RFC822)")
            for response_part in msg_data:
                if isinstance(response_part, tuple):
                    msg = email.message_from_bytes(response_part[1])
                    subject, encoding = decode_header(msg["Subject"])[0]
                    if isinstance(subject, bytes):
                        subject = subject.decode(encoding or "utf-8")
                    date_received = parsedate_to_datetime(msg["Date"])

                    print(f"Processing email: {subject} ({date_received})")

                    for part in msg.walk():
                        if part.get_content_type() == "application/pdf":
                            filename = part.get_filename()
                            if filename:
                                filename = decode_header(filename)[0][0]
                                if isinstance(filename, bytes):
                                    filename = filename.decode()
                                filepath = f"./claims/{filename}"
                                with open(filepath, "wb") as f:
                                    f.write(part.get_payload(decode=True))
                                process_claim_pdf(filepath)
        mail.logout()
    except Exception as e:
        print(f"Error fetching emails: {e}")

# Extract Text from PDF (OCR if necessary)


def extract_text_from_pdf(pdf_path):
    text = ""
    doc = fitz.open(pdf_path)

    for page in doc:
        text += page.get_text("text")

        # If no text is extracted, try OCR (for scanned documents)
        if not text.strip():
            pix = page.get_pixmap()
            img_path = f"{pdf_path}.png"
            pix.save(img_path)
            text = pytesseract.image_to_string(img_path)
            os.remove(img_path)

    return text.strip()

# Process and Validate Claim Data


def process_claim_pdf(pdf_path):
    print(f"Processing claim: {pdf_path}")
    extracted_text = extract_text_from_pdf(pdf_path)

    # Simple parsing logic (adjust based on actual claim document format)
    claim_data = {}
    lines = extracted_text.split("\n")
    for line in lines:
        if "Policy Number:" in line:
            claim_data["policy_number"] = line.split(":")[-1].strip()
        elif "Patient Name:" in line:
            claim_data["patient_name"] = line.split(":")[-1].strip()
        elif "Billing Code:" in line:
            claim_data["billing_code"] = line.split(":")[-1].strip()
        elif "Total Amount:" in line:
            claim_data["amount"] = line.split(":")[-1].strip()

    if validate_claim(claim_data):
        submit_claim(claim_data)

# Validate Claim Data


def validate_claim(claim):
    required_fields = ["policy_number",
                       "patient_name", "billing_code", "amount"]
    for field in required_fields:
        if field not in claim or not claim[field]:
            print(f"Invalid claim data: Missing {field}")
            return False
    return True

# Submit Claim to API


def submit_claim(claim):
    try:
        response = requests.post(CLAIM_API_URL, json=claim)
        if response.status_code == 200:
            print(f"Claim submitted successfully: {claim['policy_number']}")
        else:
            print(f"Failed to submit claim: {response.text}")
    except Exception as e:
        print(f"Error submitting claim: {e}")


if __name__ == "__main__":
    fetch_unread_emails()

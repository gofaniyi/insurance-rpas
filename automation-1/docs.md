# Insurance Claims Processing RPA

This Python script automates the processing of insurance claims by:
- Fetching unread emails with PDF attachments (insurance claims)
- Extracting claim details from PDFs (using text extraction and OCR for scanned documents)
- Validating the claim data (ensuring required fields are present)
- Submitting the extracted claim data to an API for processing

## Installation

Ensure you have Python installed (>=3.7), then install the required dependencies:

```bash
pip install imapclient pyzmail42 pymupdf pytesseract requests
```

### **OCR Setup (Optional, for Scanned PDFs)**
If using OCR for scanned documents, install **Tesseract OCR**:

- **macOS**: `brew install tesseract`
- **Ubuntu**: `sudo apt install tesseract-ocr`
- **Windows**: [Download here](https://github.com/UB-Mannheim/tesseract/wiki)

## Configuration

Before running the script, update the following variables inside `run.py`:

```python
IMAP_SERVER = "<EMAIL_SERVER>"  # Change to your email provider's IMAP server
EMAIL_USER = "<EMAIL_USER>"
EMAIL_PASS = "<EMAIL_PASS>"
CLAIM_API_URL = "<CLAIM_API_URL>"  # Example API
```

## How the Script Works

1. **Connects to Email Inbox** – Uses IMAP to access unread emails.
2. **Extracts PDFs** – Saves attached claim documents locally.
3. **Parses Claim Data** – Extracts text using `PyMuPDF`, with OCR fallback for scanned images.
4. **Validates Claims** – Ensures required fields are present (Policy Number, Patient Name, Billing Code, Amount).
5. **Submits to API** – Sends validated claims to an external API for processing.

## Running the Script

To run the script, execute the following command:

```bash
python run.py
```

## Possible Enhancements

- **Database Integration** – Store claims before submission for tracking.
- **Multi-Threading** – Process multiple claims concurrently for efficiency.
- **Webhook Integration** – Notify users upon successful claim submission.
- **Error Handling** – Improved logging and exception handling for failed API requests.
- **Email Notifications** – Send alerts for rejected or incomplete claims.

---

This script streamlines medical billing workflows and ensures faster claim processing. 🚀


# Invoice QC Service

## Overview
This is a full-stack Invoice Quality Control (QC) system designed to automate the processing of German B2B invoices. It extracts structured data from PDF files, validates the data against business rules, and exposes the results via a Python CLI, a REST API, and a modern Web Console.

## Schema & Validation Design

### 1. Data Schema
I designed the schema to capture the essential financial and identifying information required for accounting.
* **`invoice_number`**: (String) Unique identifier for the document (e.g., "AUFNR34343").
* **`invoice_date`**: (Date) The official date of issuance.
* **`gross_total`**: (Float) The final amount to be paid (Net + Tax).
* **`net_total`**: (Float) The amount before tax.
* **`tax_amount`**: (Float) The calculated VAT (MwSt).
* **`currency`**: (String) Defaults to "EUR".
* **`seller_name`**: (String) Vendor identification.

### 2. Validation Rules
The system applies the following logic to determine if an invoice is **Valid** or **Invalid**:
* **Completeness Rule:** Every invoice *must* have an `invoice_number` and a `gross_total`. If the extraction fails to find these, the invoice is rejected.
* **Anomaly Rule:** `gross_total` cannot be negative.
* **Business Math Rule:** If Net, Tax, and Gross values are all present, the system checks:
    `Net Total + Tax Amount ≈ Gross Total`
    (Allows for a €0.05 rounding difference).

## Architecture
The solution is split into a Python backend (logic) and a Next.js frontend (UI).

### Folder Structure
```text
invoice-qc-service/
├── invoice_qc/              # Core Python Package
│   ├── extractor.py         # PDF parsing (pdfplumber + Regex)
│   ├── validator.py         # Business logic & Error checking
│   ├── models.py            # Pydantic data schemas
│   ├── cli.py               # Command Line Interface tool
│   └── api.py               # FastAPI backend
├── frontend/                # Next.js Web Application
├── pdfs/                    # Sample PDF files
└── requirements.txt         # Python dependencies

Data Flow
Extraction: Uses pdfplumber to read text and custom Regex to handle German number formats (e.g., 1.200,50 vs 1200.50).

Validation: Checks the extracted data against the rules defined in validator.py.

Interface: Results are served via CLI or HTTP API.

Setup & Installation
1. Backend (Python)
Prerequisites: Python 3.10+

Bash

# Install dependencies
pip install -r requirements.txt

# Start the API Server
python -m uvicorn invoice_qc.api:app --reload
2. Frontend (Next.js)
Prerequisites: Node.js 18+

Bash

cd frontend
npm install
npm run dev
The web console will be available at http://localhost:3000

Usage
CLI Commands
The CLI supports three modes: Extract-only, Validate-only, and Full-Run.

Bash

# Run the full pipeline on a folder of PDFs
python -m invoice_qc.cli full-run ./pdfs --report final_report.json

# Extract only (no validation)
python -m invoice_qc.cli extract ./pdfs --output extracted.json
API Endpoints
POST /upload: Upload a PDF file to get immediate validation results.

POST /validate-json: Validate a list of raw JSON invoice objects.

GET /health: Health check endpoint.

Integration Potential
This service is designed to be "Integration-Friendly."

Microservices: The stateless API can be deployed behind a load balancer.

Async Processing: In a production environment, the extractor could run as a Celery worker, processing PDFs from an S3 bucket and pushing results to a queue.

Assumptions & Limitations
Language: The current extractor is optimized for German B2B invoices (looking for "Bestellung", "MwSt", etc.). It may not work for English or US invoices without modification.

Table Extraction: For this MVP, I simplified line-item extraction to focus on the totals validation (Net vs Gross). Complex multi-page tables might require a more advanced parser.

Currency: The system currently assumes EUR and German number formatting (comma decimals).

AI Usage Notes
Architecture: Used ChatGPT to suggest the initial Pydantic model structure and FastAPI boilerplate.

Regex Tuning: AI suggested standard currency regex, but it failed on the mixed dot/comma formats in the samples (12.16 vs 64,00). I manually wrote the parse_german_float function to handle both edge cases robustly.

Frontend: Used AI to generate the Tailwind CSS classes for the result table to ensure a clean, responsive design quickly.

Demo Video
https://drive.google.com/file/d/1h47wSP-dm0h9EGdBvtgwN0-8y81l5xHi/view?usp=sharing

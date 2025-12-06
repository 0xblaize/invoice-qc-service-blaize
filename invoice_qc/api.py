from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from typing import List
import shutil
import os

# Import your custom modules
from .models import Invoice, ValidationResult
from .extractor import parse_invoice
from .validator import validate_invoice

# 1. Initialize the App
app = FastAPI()

# 2. Add CORS (So your Website can talk to Python)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- ENDPOINTS ---

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/validate-json")
def validate_json_list(invoices: List[Invoice]):
    summary = {"total": len(invoices), "valid": 0, "invalid": 0, "results": []}
    for inv in invoices:
        res = validate_invoice(inv)
        if res.is_valid:
            summary["valid"] += 1
        else:
            summary["invalid"] += 1
        summary["results"].append(res)
    return summary

# THE FIXED UPLOAD ENDPOINT (No 'async' to prevent freezing)
@app.post("/upload")
def upload_invoice(file: UploadFile = File(...)):
    print(f"Received file: {file.filename}")  # Debug print
    
    # 1. Save uploaded file temporarily
    temp_path = f"temp_{file.filename}"
    try:
        with open(temp_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
            
        # 2. Run extraction and validation
        invoice_data = parse_invoice(temp_path)
        report = validate_invoice(invoice_data)
        
    except Exception as e:
        print(f"Error processing file: {e}")
        return {"error": str(e)}
        
    finally:
        # 3. Cleanup (Delete temp file)
        if os.path.exists(temp_path):
            try:
                os.remove(temp_path)
            except:
                pass
    
    return report
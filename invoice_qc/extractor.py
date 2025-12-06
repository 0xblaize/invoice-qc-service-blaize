import pdfplumber
import re
from datetime import datetime
from .models import Invoice

def parse_german_float(value_str: str) -> float:
    if not value_str:
        return 0.0
    clean = value_str.strip()
    # If it looks like "12.16" (dot only), just float() it
    if "." in clean and "," not in clean:
        try:
            return float(clean)
        except:
            pass
    # Otherwise treat as German: "1.200,00" -> "1200.00"
    clean = clean.replace('.', '').replace(',', '.')
    try:
        return float(clean)
    except ValueError:
        return 0.0

def extract_text_from_pdf(pdf_path: str) -> str:
    text = ""
    try:
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                text += page.extract_text() + "\n"
    except Exception as e:
        print(f"Error reading PDF: {e}")
    return text

def parse_invoice(pdf_path: str) -> Invoice:
    text = extract_text_from_pdf(pdf_path)
    
    # 1. Invoice Number
    inv_match = re.search(r'(?i)Bestellung\s+(AUFNR\w+)', text)
    invoice_number = inv_match.group(1) if inv_match else None

    # 2. Date
    date_match = re.search(r'(?i)vom\s+(\d{2}\.\d{2}\.\d{4})', text)
    invoice_date = None
    if date_match:
        try:
            dt_obj = datetime.strptime(date_match.group(1), "%d.%m.%Y")
            invoice_date = dt_obj.date()
        except:
            pass

    # 3. Totals (Matches 12,00 or 1.200,00 or 12.00)
    number_pattern = r'(\d{1,3}(?:[.,]\d{3})*[.,]\d{2})'
    
    net_match = re.search(r'(?i)Gesamtwert(?!.*inkl).*?' + number_pattern, text, re.DOTALL)
    net_total = parse_german_float(net_match.group(1)) if net_match else None

    tax_match = re.search(r'(?i)MwSt.*?' + number_pattern, text, re.DOTALL)
    tax_amount = parse_german_float(tax_match.group(1)) if tax_match else None

    gross_match = re.search(r'(?i)Gesamtwert inkl.*?' + number_pattern, text, re.DOTALL)
    gross_total = parse_german_float(gross_match.group(1)) if gross_match else None

    return Invoice(
        invoice_number=invoice_number,
        invoice_date=invoice_date,
        seller_name="Medical Equipment Deutschland",
        currency="EUR",
        net_total=net_total,
        tax_amount=tax_amount,
        gross_total=gross_total
    )
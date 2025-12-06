from typing import List
from .models import Invoice, ValidationResult

def validate_invoice(invoice: Invoice) -> ValidationResult:
    errors = []
    
    # 1. Check Invoice Number
    if not invoice.invoice_number:
        errors.append("Missing Field: invoice_number")
    
    # 2. Check Gross Total
    if invoice.gross_total is None:
        errors.append("Missing Field: gross_total")
        
    # 3. Check for Negatives
    if invoice.gross_total is not None and invoice.gross_total < 0:
        errors.append("Anomaly: Total amount cannot be negative")
        
    # 4. Check Math (Net + Tax = Gross)
    if (invoice.net_total is not None and 
        invoice.tax_amount is not None and 
        invoice.gross_total is not None):
        
        calc_gross = invoice.net_total + invoice.tax_amount
        if abs(calc_gross - invoice.gross_total) > 0.05:
            errors.append(f"Math Mismatch: {invoice.net_total} + {invoice.tax_amount} != {invoice.gross_total}")

    return ValidationResult(
        invoice_id=invoice.invoice_number or "UNKNOWN",
        is_valid=(len(errors) == 0),
        errors=errors,
        invoice_data=invoice  # <--- THIS SENDS THE DATA BACK!
    )
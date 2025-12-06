from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import date

class Invoice(BaseModel):
    invoice_number: Optional[str] = None
    invoice_date: Optional[date] = None
    seller_name: Optional[str] = None
    currency: str = "EUR"
    net_total: Optional[float] = None
    tax_amount: Optional[float] = None
    gross_total: Optional[float] = None
    
class ValidationResult(BaseModel):
    invoice_id: str
    is_valid: bool
    errors: List[str]
    invoice_data: Optional[Invoice] = None  # <--- THIS IS NEW!
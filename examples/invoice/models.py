"""Data models for invoice generation."""

from datetime import date
from typing import List, Optional
from pydantic import BaseModel, Field, validator
from enum import Enum

class Address(BaseModel):
    """Address information."""
    name: str = Field(..., description="Name of the person or company")
    street: str = Field(..., description="Street address")
    city: str = Field(..., description="City")
    state: Optional[str] = Field(None, description="State or province")
    postal_code: str = Field(..., description="Postal or ZIP code")
    country: str = Field(..., description="Country")
    email: Optional[str] = Field(None, description="Email address")
    phone: Optional[str] = Field(None, description="Phone number")

class InvoiceItem(BaseModel):
    """Line item in an invoice."""
    description: str = Field(..., description="Item description")
    quantity: float = Field(1.0, description="Quantity")
    unit_price: float = Field(..., description="Price per unit")
    tax_rate: float = Field(0.0, description="Tax rate as decimal (e.g., 0.2 for 20%)")
    
    @property
    def subtotal(self) -> float:
        """Calculate line item subtotal."""
        return self.quantity * self.unit_price
    
    @property
    def tax_amount(self) -> float:
        """Calculate tax amount for this line item."""
        return self.subtotal * self.tax_rate
    
    @property
    def total(self) -> float:
        """Calculate total including tax."""
        return self.subtotal + self.tax_amount

class PaymentMethod(str, Enum):
    """Available payment methods."""
    BANK_TRANSFER = "bank_transfer"
    CREDIT_CARD = "credit_card"
    PAYPAL = "paypal"
    CRYPTO = "crypto"
    OTHER = "other"

class InvoiceStatus(str, Enum):
    """Invoice status."""
    DRAFT = "draft"
    SENT = "sent"
    PAID = "paid"
    OVERDUE = "overdue"
    CANCELLED = "cancelled"

class InvoiceData(BaseModel):
    """Complete invoice data model."""
    # Invoice metadata
    invoice_number: str = Field(..., description="Unique invoice number")
    issue_date: date = Field(default_factory=date.today, description="Date of issue")
    due_date: date = Field(..., description="Payment due date")
    status: InvoiceStatus = Field(InvoiceStatus.DRAFT, description="Invoice status")
    notes: Optional[str] = Field(None, description="Additional notes")
    terms: Optional[str] = Field("Payment due within 30 days", description="Payment terms")
    
    # Company and client information
    company: Address = Field(..., description="Seller/issuer information")
    client: Address = Field(..., description="Client/bill to information")
    
    # Invoice items
    items: List[InvoiceItem] = Field(..., description="List of invoice items")
    
    # Payment information
    payment_method: PaymentMethod = Field(PaymentMethod.BANK_TRANSFER, description="Preferred payment method")
    payment_instructions: Optional[str] = Field(None, description="Payment instructions")
    
    # Calculated fields
    subtotal: float = Field(0.0, description="Subtotal before tax")
    tax_amount: float = Field(0.0, description="Total tax amount")
    discount: float = Field(0.0, description="Discount amount")
    total: float = Field(0.0, description="Total amount due")
    
    # Bank information (optional)
    bank_info: Optional[dict] = Field(None, description="Bank account details")
    
    class Config:
        json_encoders = {
            date: lambda d: d.isoformat(),
        }
    
    @validator('due_date')
    def due_date_must_be_after_issue_date(cls, v, values):
        if 'issue_date' in values and v < values['issue_date']:
            raise ValueError('Due date must be after issue date')
        return v
    
    @validator('items')
    def validate_items(cls, v):
        if not v:
            raise ValueError('At least one invoice item is required')
        return v
    
    def calculate_totals(self) -> None:
        """Calculate all invoice totals."""
        self.subtotal = sum(item.subtotal for item in self.items)
        self.tax_amount = sum(item.tax_amount for item in self.items)
        self.total = self.subtotal + self.tax_amount - self.discount
    
    def to_dict(self) -> dict:
        """Convert to dictionary with calculated fields."""
        self.calculate_totals()
        return self.dict()
    
    @classmethod
    def from_dict(cls, data: dict) -> 'InvoiceData':
        """Create from dictionary with validation."""
        return cls(**data)
    
    def to_json(self, **kwargs) -> str:
        """Convert to JSON string with calculated fields."""
        self.calculate_totals()
        return self.json(**kwargs)
    
    @classmethod
    def from_json(cls, json_str: str) -> 'InvoiceData':
        """Create from JSON string with validation."""
        return cls.parse_raw(json_str)

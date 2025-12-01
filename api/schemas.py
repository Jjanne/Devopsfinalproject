from typing import Optional, List
from pydantic import BaseModel, Field, EmailStr, ConfigDict

# products
class ProductCreate(BaseModel):
    title: str
    description: Optional[str] = None
    price: float = Field(ge=0)
    currency: str = "EUR"

class ProductRead(ProductCreate):
    id: int
    model_config = ConfigDict(from_attributes=True)

# customers
class CustomerCreate(BaseModel):
    email: EmailStr
    name: Optional[str] = None

class CustomerRead(CustomerCreate):
    id: int
    model_config = ConfigDict(from_attributes=True)

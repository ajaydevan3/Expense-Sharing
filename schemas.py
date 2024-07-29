from pydantic import BaseModel, EmailStr
from typing import List, Dict

class UserCreate(BaseModel):
    email: EmailStr
    name: str
    mobile_number: str

class ExpenseCreate(BaseModel):
    description: str
    amount: float
    paid_by: EmailStr
    participants: List[EmailStr]
    split_method: str
    split_details: Dict[EmailStr, float] = None

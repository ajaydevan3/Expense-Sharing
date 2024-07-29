from typing import Dict, List
from bson import ObjectId
from pydantic import EmailStr, Field, BaseModel

class UserModel(BaseModel):
    id: str = Field( alias="_id")
    email: EmailStr
    name: str
    mobile_number: str
  
  # class Config:
  #   json_schema_extra = {
  #     "examples":[
  #       {
  #         'id': 123,
  #         'fName': 'example',
  #         'lName': 'user',
  #         'email': 'email123',
  #         'phone': 'phone123',
  #         'dob': '01-01-1999',
  #         'isFav': False,
  #         'address': 'example, user, \n address',
  #         'url': 'https://example/user/profile/picture/url'
  #       }
  #     ]
  #   }
    
class Expense(BaseModel):
    id: str = Field( alias="_id")
    description: str
    amount: float
    paid_by: EmailStr
    participants: List[EmailStr]
    split_method: str
    split_details: Dict[EmailStr, float] = None
    
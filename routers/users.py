from fastapi import APIRouter, HTTPException, Depends
from pydantic import EmailStr
from typing import List
from models import UserModel
from schemas import UserCreate
from dependencies import get_db
from pymongo.collection import Collection
from bson import ObjectId as BsonObjectId

router = APIRouter(
  prefix='/users',
  tags=['users']
)

@router.post("/", response_model=UserModel)
async def create_user(user: UserCreate, db: Collection = Depends(get_db)):
    if db["users"].find_one({"email": user.email}):
        raise HTTPException(status_code=400, detail="Email already registered")
    user_data = user.dict()
    user_data["_id"] = str(BsonObjectId())
    user_id = db["users"].insert_one(user_data).inserted_id
    return db["users"].find_one({"_id": user_id})
  
@router.get("/{email}", response_model=UserModel)
async def retrieve_user(email: EmailStr, db: Collection = Depends(get_db)):
    user = db["users"].find_one({"email": email})
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

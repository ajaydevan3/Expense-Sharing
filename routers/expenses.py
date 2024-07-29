from fastapi import APIRouter, HTTPException, Depends
from typing import List

from pydantic import EmailStr
from models import Expense
from dependencies import get_db
from pymongo.collection import Collection

router = APIRouter(
  prefix='/expenses',
  tags=['expenses']
)

@router.post("/", response_model=Expense)
async def add_expense(expense, db: Collection = Depends(get_db)):
    if expense.split_method == "percentage" and sum(expense.split_details.values()) != 100:
        raise HTTPException(status_code=400, detail="Percentages must add up to 100%")
    expense_id = db["expenses"].insert_one(expense.dict()).inserted_id
    return db["expenses"].find_one({"_id": expense_id})

@router.get("/{email}", response_model=List[Expense])
async def retrieve_individual_expenses(email: EmailStr, db: Collection = Depends(get_db)):
    expenses = list(db["expenses"].find({"participants": email}))
    if not expenses:
        raise HTTPException(status_code=404, detail="No expenses found for user")
    return expenses

@router.get("/", response_model=List[Expense])
async def retrieve_overall_expenses(db: Collection = Depends(get_db)):
    return list(db["expenses"].find())

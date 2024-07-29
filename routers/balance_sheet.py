from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse
from io import StringIO
import csv
from dependencies import get_db
from pymongo.collection import Collection

router = APIRouter(
  prefix='/balance_sheet',
  tags=['balance_sheet']
)

@router.get("/download")
async def download_balance_sheet(db: Collection = Depends(get_db)):
    users = list(db["users"].find())
    expenses = list(db["expenses"].find())

    # Calculate balances
    balances = {user["email"]: 0 for user in users}
    for expense in expenses:
        amount = expense["amount"]
        paid_by = expense["paid_by"]
        participants = expense["participants"]
        split_method = expense["split_method"]
        split_details = expense["split_details"]

        if split_method == "equal":
            split_amount = amount / len(participants)
            for participant in participants:
                balances[participant] -= split_amount
            balances[paid_by] += amount
        elif split_method == "exact":
            for participant, exact_amount in split_details.items():
                balances[participant] -= exact_amount
            balances[paid_by] += amount
        elif split_method == "percentage":
            for participant, percentage in split_details.items():
                balances[participant] -= (percentage / 100) * amount
            balances[paid_by] += amount

    # Create CSV
    output = StringIO()
    writer = csv.writer(output)
    writer.writerow(["Email", "Balance"])
    for email, balance in balances.items():
        writer.writerow([email, balance])
    output.seek(0)

    return StreamingResponse(output, media_type="text/csv", headers={"Content-Disposition": "attachment; filename=balance_sheet.csv"})

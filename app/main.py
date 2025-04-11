# app/main.py
# The primary FastAPI application.
# Routes are defined here along with custom error handling to fit our API spec.

import uuid
import uvicorn
from fastapi import FastAPI, HTTPException, Request, Path
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError

from app.models import Receipt, ReceiptResponse, PointsResponse
from app.points import calculate_points
from app.store import save_receipt, get_receipt_points

app = FastAPI(
    title="Receipt Processor",
    description="A simple receipt processor",
    version="1.0.0"
)

# Custom exception handler for validation errors to return 400 status code
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=400,
        content={"detail": "The receipt is invalid."}
    )

@app.post("/receipts/process", response_model=ReceiptResponse, status_code=200)
async def process_receipt(receipt: Receipt):
    """
    Submits a receipt for processing.
    Returns a unique identifier for the receipt.
    """
    receipt_id = str(uuid.uuid4())
    points = calculate_points(receipt)
    save_receipt(receipt_id, points)
    return {"id": receipt_id}

@app.get("/receipts/{id}/points", response_model=PointsResponse, status_code=200)
async def get_points(id: str = Path(..., regex="^\\S+$", description="The ID of the receipt")):
    """
    Retrieves the points awarded for the receipt with the given ID.
    """
    points = get_receipt_points(id)
    if points is None:
        raise HTTPException(
            status_code=404,
            detail="No receipt found for that ID."
        )
    return {"points": points}

if __name__ == "__main__":
    # Running via 'uvicorn app.main:app --reload' is preferred during development.
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)

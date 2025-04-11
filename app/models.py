# app/models.py
# Pydantic models for receipt processing.

from pydantic import BaseModel, Field
from typing import List

class Item(BaseModel):
    shortDescription: str = Field(
        ...,
        description="The short product description for the item.",
        example="Mountain Dew 12PK",
        pattern="^[\\w\\s\\-]+$"
    )
    price: str = Field(
        ...,
        description="The total price paid for this item (format: NN.NN).",
        example="6.49",
        pattern="^\\d+\\.\\d{2}$"
    )

class Receipt(BaseModel):
    retailer: str = Field(
        ...,
        description="The name of the retailer or store the receipt is from.",
        example="M&M Corner Market",
        pattern="^[\\w\\s\\-&]+$"
    )
    purchaseDate: str = Field(
        ...,
        description="The date of purchase from the receipt (YYYY-MM-DD).",
        example="2022-01-01"
    )
    purchaseTime: str = Field(
        ...,
        description="The time of purchase in 24-hour format (HH:MM).",
        example="13:01"
    )
    items: List[Item] = Field(
        ...,
        min_items=1,
        description="List of purchased items."
    )
    total: str = Field(
        ...,
        description="The total amount paid on the receipt (format: NN.NN).",
        example="6.49",
        pattern="^\\d+\\.\\d{2}$"
    )

class ReceiptResponse(BaseModel):
    id: str = Field(
        ...,
        description="The unique identifier assigned to the processed receipt.",
        example="adb6b560-0eef-42bc-9d16-df48f30e89b2",
        pattern="^\\S+$"
    )

class PointsResponse(BaseModel):
    points: int = Field(
        ...,
        description="The number of points awarded for the receipt.",
        example=100
    )

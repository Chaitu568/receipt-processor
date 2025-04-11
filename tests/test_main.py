#################
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))
###################

import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

# A valid payload example (matches your schema requirements)
VALID_PAYLOAD = {
    "retailer": "M&M Corner Market",
    "purchaseDate": "2022-01-01",
    "purchaseTime": "13:01",
    "items": [
        {"shortDescription": "Mountain Dew 12PK", "price": "6.49"},
        {"shortDescription": "Emils Cheese Pizza", "price": "12.25"},
        {"shortDescription": "Knorr Creamy Chicken", "price": "1.26"},
        {"shortDescription": "Doritos Nacho Cheese", "price": "3.35"},
        {"shortDescription": "Klarbrunn 12-PK 12 FL OZ", "price": "12.00"}
    ],
    "total": "35.35"
}

# An invalid payload example (missing the 'total' field and invalid purchaseDate format)
INVALID_PAYLOAD = {
    "retailer": "M&M Corner Market",
    "purchaseDate": "01-01-2022",  # Wrong format, should be YYYY-MM-DD.
    "purchaseTime": "13:01",
    "items": [
        {"shortDescription": "Mountain Dew 12PK", "price": "6.49"}
    ]
}

def test_process_receipt_valid():
    # Test POST endpoint to process receipt
    response = client.post("/receipts/process", json=VALID_PAYLOAD)
    assert response.status_code == 200, response.text
    data = response.json()
    assert "id" in data

    # Test GET endpoint using the generated receipt id to retrieve points.
    receipt_id = data["id"]
    response_get = client.get(f"/receipts/{receipt_id}/points")
    assert response_get.status_code == 200, response_get.text
    get_data = response_get.json()
    assert "points" in get_data
    # Here you might also assert specific point values if you know what to expect.

def test_process_receipt_invalid():
    # Test POST endpoint with invalid payload returns a 400 error.
    response = client.post("/receipts/process", json=INVALID_PAYLOAD)
    assert response.status_code == 400
    data = response.json()
    # Make sure the error message exactly matches your API spec.
    assert data["detail"] == "The receipt is invalid."

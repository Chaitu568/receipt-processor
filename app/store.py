# app/store.py
# A simple in-memory storage for receipt points.
# (In a production system, I would likely use a persistent database.)

_store = {}

def save_receipt(receipt_id: str, points: int) -> None:
    _store[receipt_id] = points

def get_receipt_points(receipt_id: str) -> int:
    print(_store)
    return _store.get(receipt_id)

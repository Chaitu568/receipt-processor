# app/points.py
# This file contains the logic that calculates the points for a given receipt.
# I've kept the code straightforward and commented for clarity.

import math
import datetime
from app.models import Receipt

def calculate_points(receipt: Receipt) -> int:
    """Calculate and return the points for the provided receipt."""
    points = 0

    # Rule 1: One point per alphanumeric character in retailer's name.
    points += sum(1 for ch in receipt.retailer if ch.isalnum())

    # Rule 2: If the total is a whole dollar amount, add 50 points.
    try:
        total_val = float(receipt.total)
    except ValueError:
        total_val = 0.0
    if total_val.is_integer():
        points += 50

    # Rule 3: If total is divisible by 0.25, add 25 points.
    if abs((total_val * 100) % 25) < 1e-6:
        points += 25

    # Rule 4: Add 5 points for every two items.
    num_items = len(receipt.items)
    points += (num_items // 2) * 5

    # Rule 5: For each item, if the trimmed description's length is a multiple of 3,
    # add bonus points equal to ceiling(20% of item price).
    for item in receipt.items:
        desc = item.shortDescription.strip()
        if len(desc) % 3 == 0:
            try:
                price_val = float(item.price)
            except ValueError:
                price_val = 0.0
            bonus = math.ceil(price_val * 0.2)
            points += bonus

    # Rule 6: If the purchase day is odd, add 6 points.
    try:
        date_obj = datetime.datetime.strptime(receipt.purchaseDate, "%Y-%m-%d")
        if date_obj.day % 2 == 1:
            points += 6
    except Exception:
        # Silently ignore date parsing errors.
        pass

    # Rule 7: If purchase time is between 14:00 (inclusive) and 16:00 (exclusive), add 10 points.
    try:
        time_obj = datetime.datetime.strptime(receipt.purchaseTime, "%H:%M").time()
        if datetime.time(14, 0) <= time_obj < datetime.time(16, 0):
            points += 10
    except Exception:
        pass

    return points

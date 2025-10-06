# src/validators.py
from decimal import Decimal
from typing import Tuple
from .logging_setup import setup_logging

logger = setup_logging()

def _get_filter(symbol_info, ftype):
    for f in symbol_info.get("filters", []):
        if f.get("filterType") == ftype:
            return f
    return None

def validate_quantity(symbol_info: dict, qty: Decimal) -> Tuple[bool, str]:
    f = _get_filter(symbol_info, "LOT_SIZE")
    if not f:
        return True, "No LOT_SIZE filter"
    minQty = Decimal(f["minQty"])
    maxQty = Decimal(f["maxQty"])
    step = Decimal(f["stepSize"])
    if qty < minQty: return False, f"Qty {qty} < min {minQty}"
    if qty > maxQty: return False, f"Qty {qty} > max {maxQty}"
    if (qty % step) != 0: return False, f"Qty {qty} not multiple of {step}"
    return True, "Quantity OK"

def validate_price(symbol_info: dict, price: Decimal) -> Tuple[bool, str]:
    f = _get_filter(symbol_info, "PRICE_FILTER")
    if not f:
        return True, "No PRICE_FILTER"
    minP = Decimal(f["minPrice"])
    maxP = Decimal(f.get("maxPrice", "1e18"))
    tick = Decimal(f["tickSize"])
    if price < minP: return False, f"Price {price} < min {minP}"
    if price > maxP: return False, f"Price {price} > max {maxP}"
    if (price % tick) != 0: return False, f"Price {price} not multiple of {tick}"
    return True, "Price OK"

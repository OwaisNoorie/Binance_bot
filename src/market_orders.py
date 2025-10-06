# src/market_orders.py
import argparse
from decimal import Decimal
from .binance_client import BinanceFuturesClient, BinanceClientError
from .validators import validate_quantity
from .logging_setup import setup_logging

logger = setup_logging()

def main():
    parser = argparse.ArgumentParser(description="Place Futures Market Order")
    parser.add_argument("--symbol", required=True, help="e.g. BTCUSDT")
    parser.add_argument("--side", required=True, choices=["BUY", "SELL"])
    parser.add_argument("--quantity", required=True, type=float)
    args = parser.parse_args()

    client = BinanceFuturesClient()
    symbol_info = client.get_symbol_info(args.symbol.upper())
    if not symbol_info:
        logger.error(f"Symbol {args.symbol} not found")
        print("Invalid symbol")
        return

    qty = Decimal(str(args.quantity))
    ok, msg = validate_quantity(symbol_info, qty)
    if not ok:
        logger.error(msg)
        print("Validation failed:", msg)
        return

    try:
        res = client.place_market_order(args.symbol.upper(), args.side.upper(), qty)
        print("Order success! Check bot.log")
    except BinanceClientError as e:
        print("Order failed:", e)

if __name__ == "__main__":
    main()

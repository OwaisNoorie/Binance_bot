# src/binance_client.py
from decimal import Decimal
from binance.client import Client
from binance.exceptions import BinanceAPIException, BinanceRequestException
from .config import API_KEY, API_SECRET, TESTNET, REQUEST_TIMEOUT
from .logging_setup import setup_logging

logger = setup_logging()

class BinanceClientError(Exception):
    pass

class BinanceFuturesClient:
    def __init__(self):
        if not API_KEY or not API_SECRET:
            raise BinanceClientError("API_KEY or API_SECRET missing in .env")

        self.client = Client(API_KEY, API_SECRET)

        # Force Futures Testnet endpoint if TESTNET=True
        if TESTNET:
            self.client.FUTURES_URL = "https://testnet.binancefuture.com/fapi"

    def get_symbol_info(self, symbol: str):
        try:
            info = self.client.futures_exchange_info()
            for s in info["symbols"]:
                if s["symbol"] == symbol:
                    return s
            return None
        except Exception as e:
            logger.exception("Error fetching symbol info")
            raise BinanceClientError(str(e))

    def place_market_order(self, symbol: str, side: str, quantity: Decimal):
        try:
            res = self.client.futures_create_order(
                symbol=symbol,
                side=side,
                type="MARKET",
                quantity=float(quantity),
                recvWindow=REQUEST_TIMEOUT * 1000,
            )
            logger.info(f"Market order placed: {res}")
            return res
        except (BinanceAPIException, BinanceRequestException) as e:
            logger.exception("Binance API error")
            raise BinanceClientError(str(e))

    def place_limit_order(self, symbol: str, side: str, quantity: Decimal, price: Decimal):
        try:
            res = self.client.futures_create_order(
                symbol=symbol,
                side=side,
                type="LIMIT",
                timeInForce="GTC",
                quantity=float(quantity),
                price=str(price),
                recvWindow=REQUEST_TIMEOUT * 1000,
            )
            logger.info(f"Limit order placed: {res}")
            return res
        except (BinanceAPIException, BinanceRequestException) as e:
            logger.exception("Binance API error")
            raise BinanceClientError(str(e))

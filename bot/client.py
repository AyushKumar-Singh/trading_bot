"""
Binance API client wrapper module.

Provides a wrapper around the python-binance library configured
for Binance Futures Testnet (USDT-M).
"""

import os
from typing import Any, Optional

from binance.client import Client
from binance.exceptions import BinanceAPIException, BinanceRequestException
from dotenv import load_dotenv

from bot.logging_config import setup_logging

# Load environment variables from .env file
load_dotenv()

logger = setup_logging()

TESTNET_BASE_URL: str = "https://testnet.binancefuture.com"


class BinanceClient:
    """Wrapper around python-binance for Binance Futures Testnet.

    Reads API credentials from environment variables and configures
    the client to use the Futures Testnet endpoint.

    Attributes:
        client: The underlying python-binance Client instance.
    """

    def __init__(self) -> None:
        """Initialize the Binance Futures Testnet client.

        Reads BINANCE_API_KEY and BINANCE_SECRET_KEY from environment
        variables and configures the client for testnet usage.

        Raises:
            EnvironmentError: If API credentials are not set in
                environment variables.
        """
        api_key: Optional[str] = os.environ.get("BINANCE_API_KEY")
        api_secret: Optional[str] = os.environ.get("BINANCE_SECRET_KEY")

        if not api_key or not api_secret:
            error_msg = (
                "Binance API credentials not found. "
                "Set BINANCE_API_KEY and BINANCE_SECRET_KEY "
                "environment variables."
            )
            logger.error(error_msg)
            raise EnvironmentError(error_msg)

        self.client: Client = Client(api_key, api_secret, testnet=True)
        self.client.FUTURES_URL = TESTNET_BASE_URL

        logger.info("Binance Futures Testnet client initialized successfully")

    def place_order(
        self,
        symbol: str,
        side: str,
        order_type: str,
        quantity: float,
        price: Optional[float] = None,
    ) -> dict[str, Any]:
        """Place an order on Binance Futures Testnet.

        Constructs the order parameters and sends them to the
        Binance Futures API. Logs both the request and response.

        Args:
            symbol: Trading pair symbol (e.g. 'BTCUSDT').
            side: Order side ('BUY' or 'SELL').
            order_type: Type of order ('MARKET' or 'LIMIT').
            quantity: Order quantity.
            price: Order price (required for LIMIT orders).

        Returns:
            dict: The API response containing order details.

        Raises:
            BinanceAPIException: If the Binance API returns an error.
            BinanceRequestException: If there is a network issue.
            Exception: For any other unexpected errors.
        """
        order_params: dict[str, Any] = {
            "symbol": symbol,
            "side": side,
            "type": order_type,
            "quantity": quantity,
        }

        if order_type == "LIMIT":
            order_params["price"] = price
            order_params["timeInForce"] = "GTC"

        logger.info(
            f"Placing order {symbol} {side} {order_type} "
            f"quantity={quantity}"
            + (f" price={price}" if price else "")
        )
        logger.info(f"API request parameters: {order_params}")

        try:
            response: dict[str, Any] = self.client.futures_create_order(
                **order_params
            )
            logger.info(f"API response: {response}")
            return response

        except BinanceAPIException as e:
            logger.error(f"Binance API error: {e.message} (code: {e.code})")
            raise

        except BinanceRequestException as e:
            logger.error(f"Network error communicating with Binance: {e}")
            raise

        except Exception as e:
            logger.error(f"Unexpected error placing order: {e}")
            raise

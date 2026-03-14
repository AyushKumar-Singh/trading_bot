"""
Order business logic module.

Contains the core order placement logic that validates inputs,
optionally performs a dry run, and delegates to the Binance
client wrapper for actual order execution.
"""

from typing import Any, Optional

from bot.client import BinanceClient
from bot.logging_config import setup_logging
from bot.validators import validate_order_params

logger = setup_logging()


def place_order(
    symbol: str,
    side: str,
    order_type: str,
    quantity: float,
    price: Optional[float] = None,
    dry_run: bool = False,
) -> Optional[dict[str, Any]]:
    """Validate inputs and place an order on Binance Futures Testnet.

    This function serves as the business logic layer between the CLI
    and the Binance API client. It validates all parameters, handles
    dry-run mode, and delegates to the client for order execution.

    Args:
        symbol: Trading pair symbol (e.g. 'BTCUSDT').
        side: Order side ('BUY' or 'SELL').
        order_type: Type of order ('MARKET' or 'LIMIT').
        quantity: Order quantity.
        price: Order price (required for LIMIT orders).
        dry_run: If True, validate and log but do not send the order.

    Returns:
        dict: The API response from Binance if the order is placed.
        None: If dry_run is True.

    Raises:
        ValueError: If any order parameter is invalid.
        EnvironmentError: If API credentials are missing.
        Exception: For API or network errors during order placement.
    """
    # Step 1: Validate all order parameters
    validate_order_params(symbol, side, order_type, quantity, price)

    # Step 2: Print order request summary
    print("\n===== ORDER REQUEST =====")
    print(f"Symbol: {symbol}")
    print(f"Side: {side}")
    print(f"Type: {order_type}")
    print(f"Quantity: {quantity}")
    if order_type == "LIMIT" and price is not None:
        print(f"Price: {price}")

    # Step 3: Handle dry-run mode
    if dry_run:
        logger.info(
            f"DRY RUN — Order validated but not sent: "
            f"{symbol} {side} {order_type} quantity={quantity}"
            + (f" price={price}" if price else "")
        )
        print("\nDRY RUN MODE — No order sent to Binance")
        return None

    # Step 4: Place the order via the client
    client = BinanceClient()
    response: dict[str, Any] = client.place_order(
        symbol=symbol,
        side=side,
        order_type=order_type,
        quantity=quantity,
        price=price,
    )

    return response

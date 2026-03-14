"""
Input validation module.

Provides validation functions for order parameters before
they are sent to the Binance Futures API.
"""

from typing import Optional

from bot.logging_config import setup_logging

logger = setup_logging()

VALID_SIDES: set[str] = {"BUY", "SELL"}
VALID_ORDER_TYPES: set[str] = {"MARKET", "LIMIT"}


def validate_symbol(symbol: str) -> None:
    """Validate that the trading symbol is uppercase.

    Args:
        symbol: Trading pair symbol (e.g. 'BTCUSDT').

    Raises:
        ValueError: If the symbol is not uppercase.
    """
    if symbol != symbol.upper():
        error_msg = f"Symbol must be uppercase. Got: '{symbol}'"
        logger.error(f"Validation error: {error_msg}")
        raise ValueError(error_msg)


def validate_side(side: str) -> None:
    """Validate that the order side is BUY or SELL.

    Args:
        side: Order side ('BUY' or 'SELL').

    Raises:
        ValueError: If the side is not BUY or SELL.
    """
    if side not in VALID_SIDES:
        error_msg = f"Side must be BUY or SELL. Got: '{side}'"
        logger.error(f"Validation error: {error_msg}")
        raise ValueError(error_msg)


def validate_order_type(order_type: str) -> None:
    """Validate that the order type is MARKET or LIMIT.

    Args:
        order_type: Type of order ('MARKET' or 'LIMIT').

    Raises:
        ValueError: If the order type is not MARKET or LIMIT.
    """
    if order_type not in VALID_ORDER_TYPES:
        error_msg = f"Type must be MARKET or LIMIT. Got: '{order_type}'"
        logger.error(f"Validation error: {error_msg}")
        raise ValueError(error_msg)


def validate_quantity(quantity: float) -> None:
    """Validate that the quantity is greater than zero.

    Args:
        quantity: Order quantity.

    Raises:
        ValueError: If the quantity is not greater than 0.
    """
    if quantity <= 0:
        error_msg = f"Quantity must be greater than 0. Got: {quantity}"
        logger.error(f"Validation error: {error_msg}")
        raise ValueError(error_msg)


def validate_price(order_type: str, price: Optional[float]) -> None:
    """Validate the price based on the order type.

    For LIMIT orders, price is required and must be greater than 0.
    For MARKET orders, price is ignored.

    Args:
        order_type: Type of order ('MARKET' or 'LIMIT').
        price: Order price (required for LIMIT orders).

    Raises:
        ValueError: If price is missing or invalid for LIMIT orders.
    """
    if order_type == "LIMIT":
        if price is None:
            error_msg = "Price is required for LIMIT orders"
            logger.error(f"Validation error: {error_msg}")
            raise ValueError(error_msg)
        if price <= 0:
            error_msg = f"Price must be greater than 0. Got: {price}"
            logger.error(f"Validation error: {error_msg}")
            raise ValueError(error_msg)


def validate_order_params(
    symbol: str,
    side: str,
    order_type: str,
    quantity: float,
    price: Optional[float] = None,
) -> None:
    """Validate all order parameters.

    Runs all individual validation checks in sequence.

    Args:
        symbol: Trading pair symbol (e.g. 'BTCUSDT').
        side: Order side ('BUY' or 'SELL').
        order_type: Type of order ('MARKET' or 'LIMIT').
        quantity: Order quantity.
        price: Order price (required for LIMIT orders).

    Raises:
        ValueError: If any validation check fails.
    """
    validate_symbol(symbol)
    validate_side(side)
    validate_order_type(order_type)
    validate_quantity(quantity)
    validate_price(order_type, price)
    logger.info("All order parameters validated successfully")

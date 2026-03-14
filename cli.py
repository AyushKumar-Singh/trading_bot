"""
CLI entry point for the Trading Bot.

Provides an argparse-based command-line interface for placing
MARKET and LIMIT orders on Binance Futures Testnet.
"""

import argparse
import sys
from typing import Any, Optional

from binance.exceptions import BinanceAPIException, BinanceRequestException

from bot.logging_config import setup_logging
from bot.orders import place_order

logger = setup_logging()


def build_parser() -> argparse.ArgumentParser:
    """Build and return the argument parser for the CLI.

    Returns:
        argparse.ArgumentParser: Configured argument parser with
            the 'order' subcommand and all required flags.
    """
    parser = argparse.ArgumentParser(
        description="Trading Bot CLI — Place orders on Binance Futures Testnet",
    )

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # 'order' subcommand
    order_parser = subparsers.add_parser(
        "order",
        help="Place a MARKET or LIMIT order",
    )

    order_parser.add_argument(
        "--symbol",
        type=str,
        required=True,
        help="Trading pair symbol (e.g. BTCUSDT)",
    )
    order_parser.add_argument(
        "--side",
        type=str,
        required=True,
        choices=["BUY", "SELL"],
        help="Order side: BUY or SELL",
    )
    order_parser.add_argument(
        "--type",
        type=str,
        required=True,
        choices=["MARKET", "LIMIT"],
        dest="order_type",
        help="Order type: MARKET or LIMIT",
    )
    order_parser.add_argument(
        "--quantity",
        type=float,
        required=True,
        help="Order quantity (must be > 0)",
    )
    order_parser.add_argument(
        "--price",
        type=float,
        required=False,
        default=None,
        help="Order price (required for LIMIT orders)",
    )
    order_parser.add_argument(
        "--dry-run",
        action="store_true",
        default=False,
        help="Validate and log the order without sending it to Binance",
    )

    return parser


def print_order_response(response: dict[str, Any]) -> None:
    """Print the formatted order response to the console.

    Args:
        response: The API response dictionary from Binance.
    """
    print("\n===== ORDER RESPONSE =====")
    print(f"OrderId: {response.get('orderId', 'N/A')}")
    print(f"Status: {response.get('status', 'N/A')}")
    print(f"ExecutedQty: {response.get('executedQty', '0')}")
    print(f"AvgPrice: {response.get('avgPrice', '0')}")
    print("\nSUCCESS")


def main() -> None:
    """Main entry point for the CLI application.

    Parses command-line arguments, delegates to the order logic,
    and handles all exceptions with clear error messages and logging.
    """
    parser = build_parser()
    args = parser.parse_args()

    if args.command is None:
        parser.print_help()
        sys.exit(1)

    if args.command == "order":
        try:
            response: Optional[dict[str, Any]] = place_order(
                symbol=args.symbol,
                side=args.side,
                order_type=args.order_type,
                quantity=args.quantity,
                price=args.price,
                dry_run=args.dry_run,
            )

            if response is not None:
                print_order_response(response)

        except ValueError as e:
            logger.error(f"Validation error: {e}")
            print(f"\nERROR: {e}")
            sys.exit(1)

        except EnvironmentError as e:
            logger.error(f"Environment error: {e}")
            print(f"\nERROR: {e}")
            sys.exit(1)

        except BinanceAPIException as e:
            logger.error(f"Binance API error: {e.message}")
            print(f"\nERROR: Binance API error — {e.message}")
            sys.exit(1)

        except BinanceRequestException as e:
            logger.error(f"Network error: {e}")
            print(f"\nERROR: Network failure — {e}")
            sys.exit(1)

        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            print(f"\nERROR: Unexpected error — {e}")
            sys.exit(1)


if __name__ == "__main__":
    main()

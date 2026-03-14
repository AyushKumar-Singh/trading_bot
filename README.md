# Trading Bot CLI

A simplified trading bot CLI application that places **MARKET** and **LIMIT** orders on **Binance Futures Testnet (USDT-M)**.

Built with Python 3.10 and the [python-binance](https://github.com/sammchardy/python-binance) library.

> **Note:** This project connects to the Binance Futures **Testnet** at `https://testnet.binancefuture.com`. No real funds are used.

---

## Project Structure

```
trading_bot/
  bot/
    __init__.py          # Package initializer
    client.py            # Binance API wrapper
    orders.py            # Order business logic
    validators.py        # Input validation
    logging_config.py    # Logging setup
  cli.py                 # CLI entry point
  .env                   # API credentials (do not commit)
  README.md              # Project documentation
  requirements.txt       # Python dependencies
```

---

## Setup Instructions

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure API Credentials

The bot loads API credentials from a `.env` file in the project root. Get your testnet keys from the [Binance Futures Testnet](https://testnet.binancefuture.com).

Create or edit the `.env` file:

```env
BINANCE_API_KEY=your_api_key
BINANCE_SECRET_KEY=your_secret_key
```

> **Important:** Never commit the `.env` file to version control. Add it to `.gitignore`.

---

## Usage

All commands are run from the `trading_bot/` directory.

### Place a MARKET Order

```bash
python cli.py order --symbol BTCUSDT --side BUY --type MARKET --quantity 0.01
```

### Place a LIMIT Order

```bash
python cli.py order --symbol BTCUSDT --side SELL --type LIMIT --quantity 0.01 --price 60000
```

### Dry-Run Mode

Validate and log the order **without** sending it to Binance:

```bash
python cli.py order --symbol BTCUSDT --side BUY --type MARKET --quantity 0.01 --dry-run
```

---

## Output Examples

### Successful Order

```
===== ORDER REQUEST =====
Symbol: BTCUSDT
Side: BUY
Type: MARKET
Quantity: 0.01

===== ORDER RESPONSE =====
OrderId: 123456
Status: NEW
ExecutedQty: 0
AvgPrice: 0

SUCCESS
```

### Dry-Run Mode

```
===== ORDER REQUEST =====
Symbol: BTCUSDT
Side: BUY
Type: MARKET
Quantity: 0.01

DRY RUN MODE — No order sent to Binance
```

### Error

```
ERROR: Price is required for LIMIT orders
```

---

## Logging

All activity is logged to `logs/trading_bot.log`. The `logs/` directory is created automatically on first run.

Log entries include timestamp, level, and message:

```
2026-03-14 10:31:22 - INFO - Placing order BTCUSDT BUY MARKET quantity=0.01
```

---

## Architecture

```
CLI (cli.py)  →  Order Logic (orders.py)  →  API Wrapper (client.py)
                       ↑
               Validators (validators.py)
```

- **cli.py** — Parses CLI arguments and formats output.
- **orders.py** — Validates input and orchestrates order placement.
- **client.py** — Wraps the python-binance library for Futures Testnet.
- **validators.py** — Enforces input rules (symbol, side, type, quantity, price).
- **logging_config.py** — Configures file and console logging.

---

## Requirements

- Python 3.10+
- `python-binance`
- `python-dotenv`
- `requests`

---

## License

This project is for demonstration and assessment purposes.

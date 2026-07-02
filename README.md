# Trading Bot - Binance Futures Testnet

Small Python app to place MARKET and LIMIT orders on Binance Futures Testnet (USDT-M),
with a CLI and an optional Streamlit UI.

## Project structure

```
trading_bot/
  bot/
    __init__.py
    client.py          # builds the Binance client, points it at the testnet
    orders.py          # actually places the order
    validators.py       # checks CLI/UI input before it hits the API
    logging_config.py   # logging setup, writes to logs/trading_bot.log
  cli.py                # CLI entry point (typer)
  streamlit_app.py      # optional UI (bonus)
  requirements.txt
  .env.example
  logs/                 # created automatically, holds trading_bot.log
```

## Setup

1. Get testnet API keys from https://testnet.binancefuture.com (register, then
   generate an API key/secret from the account page). These are separate from
   your real Binance account.

2. Create a virtual environment and install dependencies:

   ```
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

3. Copy `.env.example` to `.env` and paste in your testnet keys:

   ```
   cp .env.example .env
   ```

   ```
   BINANCE_API_KEY=your_key
   BINANCE_API_SECRET=your_secret
   ```

## Running - CLI

Market order:
```
python cli.py place --symbol BTCUSDT --side BUY --type MARKET --quantity 0.01
```

Limit order:
```
python cli.py place --symbol BTCUSDT --side SELL --type LIMIT --quantity 0.01 --price 60000
```

`--help` works on both the app and the command if you forget the flags:
```
python cli.py place --help
```

## Running - UI (bonus)

```
streamlit run streamlit_app.py
```

This opens a form in the browser with the same fields as the CLI (symbol, side,
type, quantity, price). It calls the same `place_order` function underneath, so
behaviour and logging are identical to the CLI.

## Logging

Every request, response, and error is logged to `logs/trading_bot.log` (and also
printed to the console). Example line:

```
2026-07-02 10:14:03 | INFO | Sending order request: {'symbol': 'BTCUSDT', 'side': 'BUY', 'type': 'MARKET', 'quantity': 0.01}
2026-07-02 10:14:04 | INFO | Order response: {'orderId': 12345, 'status': 'FILLED', ...}
```

## Assumptions

- Only USDT-M futures pairs are supported (symbol must end in `USDT`), since that's
  what the task asked for.
- LIMIT orders use `GTC` (good till cancelled) as the time-in-force, since the task
  didn't specify one and it's the most common default.
- Quantity/price precision (lot size, tick size) is not auto-rounded to each symbol's
  exchange rules - if Binance rejects an order for precision reasons, the error message
  from the API is logged and shown as-is rather than silently "fixed".
- No order cancellation/query commands were added since the task only asked for
  placing orders.

## Known limitation

If your IP is geo-blocked from Binance testnet endpoints, you'll see a connection
error. Using a VPN or checking https://testnet.binancefuture.com in a browser first
usually confirms whether that's the issue.

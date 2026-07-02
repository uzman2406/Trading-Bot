"""
Thin wrapper around python-binance so the rest of the app doesn't
need to know how the client is configured (keys, testnet url, etc).
"""

import os
from binance.client import Client
from dotenv import load_dotenv

load_dotenv()


def get_client() -> Client:
    api_key = os.getenv("BINANCE_API_KEY")
    api_secret = os.getenv("BINANCE_API_SECRET")

    if not api_key or not api_secret:
        raise ValueError(
            "BINANCE_API_KEY / BINANCE_API_SECRET not found. "
            "Copy .env.example to .env and fill in your testnet keys."
        )

    # testnet=True makes python-binance route futures calls to
    # testnet.binancefuture.com automatically - no manual URL needed.
    client = Client(api_key, api_secret, testnet=True)

    return client

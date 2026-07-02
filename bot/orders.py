import logging
from binance.exceptions import BinanceAPIException, BinanceRequestException

logger = logging.getLogger("trading_bot")


def place_order(client, symbol, side, order_type, quantity, price=None):
    params = {
        "symbol": symbol,
        "side": side,
        "type": order_type,
        "quantity": float(quantity),
    }

    if order_type == "LIMIT":
        params["price"] = float(price)
        params["timeInForce"] = "GTC"  # good till cancelled, simplest option for a limit order

    logger.info(f"Sending order request: {params}")

    try:
        response = client.futures_create_order(**params)
        logger.info(f"Order response: {response}")
        return response

    except (BinanceAPIException, BinanceRequestException) as e:
        logger.error(f"Binance rejected the order: {e}")
        raise

    except Exception as e:
        logger.error(f"Network/unexpected error placing order: {e}")
        raise

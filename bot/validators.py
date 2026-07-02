"""
Basic input validation, kept separate from the CLI/UI so both the
Typer CLI and the Streamlit app can share the same rules.
"""

from decimal import Decimal, InvalidOperation

VALID_SIDES = {"BUY", "SELL"}
VALID_TYPES = {"MARKET", "LIMIT"}


class ValidationError(Exception):
    pass


def validate_order_input(symbol, side, order_type, quantity, price=None):
    symbol = str(symbol).upper().strip()
    side = str(side).upper().strip()
    order_type = str(order_type).upper().strip()

    if not symbol.endswith("USDT"):
        raise ValidationError(
            f"'{symbol}' doesn't look like a USDT-M pair, expected something like BTCUSDT"
        )

    if side not in VALID_SIDES:
        raise ValidationError(f"side must be BUY or SELL, got '{side}'")

    if order_type not in VALID_TYPES:
        raise ValidationError(f"order type must be MARKET or LIMIT, got '{order_type}'")

    try:
        quantity = Decimal(str(quantity))
    except InvalidOperation:
        raise ValidationError(f"quantity '{quantity}' is not a valid number")

    if quantity <= 0:
        raise ValidationError("quantity must be greater than 0")

    if order_type == "LIMIT":
        if price is None or str(price).strip() == "":
            raise ValidationError("price is required for LIMIT orders")
        try:
            price = Decimal(str(price))
        except InvalidOperation:
            raise ValidationError(f"price '{price}' is not a valid number")
        if price <= 0:
            raise ValidationError("price must be greater than 0")
    else:
        price = None

    return symbol, side, order_type, quantity, price

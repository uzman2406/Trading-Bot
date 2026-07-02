"""
CLI entry point. Example:

python cli.py --symbol BTCUSDT --side BUY --type MARKET --quantity 0.01
python cli.py --symbol BTCUSDT --side SELL --type LIMIT --quantity 0.01 --price 60000
"""

import typer

from bot.logging_config import setup_logger
from bot.client import get_client
from bot.validators import validate_order_input, ValidationError
from bot.orders import place_order

logger = setup_logger()


def place(
    symbol: str = typer.Option(..., help="Trading pair, e.g. BTCUSDT"),
    side: str = typer.Option(..., help="BUY or SELL"),
    order_type: str = typer.Option(..., "--type", help="MARKET or LIMIT"),
    quantity: float = typer.Option(..., help="Order quantity"),
    price: float = typer.Option(None, help="Price, required for LIMIT orders"),
):
    try:
        symbol, side, order_type, quantity, price = validate_order_input(
            symbol, side, order_type, quantity, price
        )
    except ValidationError as e:
        typer.secho(f"Input error: {e}", fg=typer.colors.RED)
        logger.error(f"Validation failed: {e}")
        raise typer.Exit(code=1)

    typer.echo("Order request:")
    typer.echo(f"  symbol   : {symbol}")
    typer.echo(f"  side     : {side}")
    typer.echo(f"  type     : {order_type}")
    typer.echo(f"  quantity : {quantity}")
    if price:
        typer.echo(f"  price    : {price}")

    try:
        client = get_client()
        response = place_order(client, symbol, side, order_type, quantity, price)
    except Exception as e:
        typer.secho(f"\nOrder failed: {e}", fg=typer.colors.RED)
        raise typer.Exit(code=1)

    typer.secho("\nOrder placed successfully", fg=typer.colors.GREEN)
    typer.echo(f"  orderId     : {response.get('orderId')}")
    typer.echo(f"  status      : {response.get('status')}")
    typer.echo(f"  executedQty : {response.get('executedQty')}")

    avg_price = response.get("avgPrice")
    if avg_price and float(avg_price) > 0:
        typer.echo(f"  avgPrice    : {avg_price}")


if __name__ == "__main__":
    typer.run(place)

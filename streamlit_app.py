"""
Bonus: a small Streamlit UI on top of the same order logic used by
the CLI. Run with: streamlit run streamlit_app.py
"""

import streamlit as st

from bot.logging_config import setup_logger
from bot.client import get_client
from bot.validators import validate_order_input, ValidationError
from bot.orders import place_order

logger = setup_logger()

st.set_page_config(page_title="Futures Testnet Bot", page_icon="📈")

st.title("Binance Futures Testnet Bot")
st.caption("Places orders on the Binance Futures TESTNET only, not real funds.")

with st.form("order_form"):
    col1, col2 = st.columns(2)
    with col1:
        symbol = st.text_input("Symbol", value="BTCUSDT")
        side = st.selectbox("Side", ["BUY", "SELL"])
    with col2:
        order_type = st.selectbox("Order type", ["MARKET", "LIMIT"])
        quantity = st.number_input("Quantity", min_value=0.0, value=0.01, step=0.001, format="%f")

    price = None
    if order_type == "LIMIT":
        price = st.number_input("Price", min_value=0.0, value=0.0, step=0.1, format="%f")

    submitted = st.form_submit_button("Place order")

if submitted:
    try:
        v_symbol, v_side, v_type, v_qty, v_price = validate_order_input(
            symbol, side, order_type, quantity, price
        )
    except ValidationError as e:
        st.error(f"Input error: {e}")
        st.stop()

    st.write("Order request")
    st.json(
        {
            "symbol": v_symbol,
            "side": v_side,
            "type": v_type,
            "quantity": float(v_qty),
            "price": float(v_price) if v_price else None,
        }
    )

    try:
        client = get_client()
        response = place_order(client, v_symbol, v_side, v_type, v_qty, v_price)
    except Exception as e:
        st.error(f"Order failed: {e}")
        st.stop()

    st.success("Order placed successfully")
    st.write("Order response")
    st.json(response)

st.divider()
st.caption(f"Logs are written to logs/trading_bot.log")

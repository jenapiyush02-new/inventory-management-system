import streamlit as st
from api import update_stock

st.title("Stock Movement")

if "token" not in st.session_state:
    st.stop()

warehouse_id = st.text_input("Warehouse ID")
item_id = st.text_input("Item ID")

movement_type = st.selectbox(
    "Movement",
    ["IN", "OUT", "ADJUST"]
)

quantity = st.number_input("Quantity", min_value=1)

if st.button("Submit Movement"):

    payload = {
        "warehouse_id": warehouse_id,
        "item_id": item_id,
        "quantity": quantity,
        "movement_type": movement_type
    }

    response = update_stock(st.session_state["token"], payload)

    st.write(response)
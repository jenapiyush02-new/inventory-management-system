import streamlit as st
from api import get_warehouses, get_inventory
import asyncio
from websocket_client import start_listener

st.title("Dashboard")

if "token" not in st.session_state:
    st.warning("Login first")
    st.stop()

role = st.session_state.get("role")
st.write(f"Logged in as: **{role}**")

token = st.session_state["token"]

warehouses_response = get_warehouses(token)

if warehouses_response.status_code == 200:
    warehouses = warehouses_response.json()
else:
    st.error("Failed to fetch warehouses")
    st.stop()

warehouse_dict = {w["name"]: w["id"] for w in warehouses}

selected = st.selectbox("Select Warehouse", list(warehouse_dict.keys()))

if selected:
    inventory_response = get_inventory(token, warehouse_dict[selected])

    if inventory_response.status_code == 200:
        st.table(inventory_response.json())
        
placeholder = st.empty()

# def handle_message(data):
#     placeholder.success(f"Live Update: {data}")

# if st.button("Start Live Updates"):
#     asyncio.run(listen(handle_message))


if "listener_started" not in st.session_state:
    st.session_state["listener_started"] = False

placeholder = st.empty()

def handle_message(data):
    placeholder.success(f"Live Update: {data}")

if st.button("Start Live Updates"):
    if not st.session_state["listener_started"]:
        start_listener(handle_message)
        st.session_state["listener_started"] = True
        st.success("Live updates started")
        


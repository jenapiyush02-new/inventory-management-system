import streamlit as st
import requests
from api import BASE_URL

st.title("Create Warehouse")

if "token" not in st.session_state:
    st.stop()

headers = {"Authorization": f"Bearer {st.session_state['token']}"}

name = st.text_input("Warehouse Name")
location = st.text_input("Location")

if st.button("Create Warehouse"):

    payload = {
        "name": name,
        "location": location
    }

    response = requests.post(
        f"{BASE_URL}/items/warehouse",
        headers=headers,
        json=payload
    )

    if response.status_code == 200:
        st.success("Warehouse created")
    else:
        st.error(response.text)
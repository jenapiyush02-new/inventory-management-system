import streamlit as st
import requests
from api import BASE_URL

st.title("View Data")

# guard
if "token" not in st.session_state:
    st.warning("Please login first")
    st.stop()

headers = {"Authorization": f"Bearer {st.session_state['token']}"}

option = st.selectbox(
    "Select Data",
    ["Items"]
)

if option == "Items":

    response = requests.get(
        f"{BASE_URL}/items/items",
        headers=headers
    )

    if response.status_code == 200:
        data = response.json()
        st.table(data)
    else:
        st.error(response.text)
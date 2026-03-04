import streamlit as st
import requests
from api import BASE_URL

st.title("Stock Movement History")

if "token" not in st.session_state:
    st.warning("Login required")
    st.stop()

headers = {"Authorization": f"Bearer {st.session_state['token']}"}

response = requests.get(
    f"{BASE_URL}/items/movements",
    headers=headers
)

if response.status_code == 200:
    st.table(response.json())
else:
    st.error(response.text)
import streamlit as st
import requests
from api import BASE_URL

st.title("User Management")

if st.session_state.get("role") != "admin":
    st.stop()

headers = {"Authorization": f"Bearer {st.session_state['token']}"}

response = requests.get(
    f"{BASE_URL}/users",
    headers=headers
)

st.table(response.json())
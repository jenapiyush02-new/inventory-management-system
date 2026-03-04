import streamlit as st
import requests
from api import BASE_URL

st.title("Create User")

if "role" not in st.session_state or st.session_state["role"] != "admin":
    st.error("Admin only")
    st.stop()

username = st.text_input("Username")
email = st.text_input("Email")
password = st.text_input("Password", type="password")

role = st.selectbox("Role", ["manager", "viewer"])

if st.button("Create User"):

    payload = {
        "username": username,
        "email": email,
        "password": password,
        "role": role
    }

    response = requests.post(
        f"{BASE_URL}/auth/register",
        json=payload
    )

    if response.status_code == 200:
        st.success("User created")
    else:
        st.error(response.text)
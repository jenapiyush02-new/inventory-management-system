import streamlit as st
from api import login
import jwt 
st.title("Login")

username = st.text_input("Username")
password = st.text_input("Password", type="password")

if st.button("Login"):
    response = login(username, password)

    if response.status_code == 200:
        data = response.json()
        token = data["access_token"]

        decoded = jwt.decode(token, options={"verify_signature": False})

        st.session_state["token"] = token
        st.session_state["role"] = decoded.get("role")

        st.success("Login successful")
    
    else:
        st.error("Invalid credentials")
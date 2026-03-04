import streamlit as st
import requests
from api import BASE_URL

st.title("Create Item")

if "token" not in st.session_state:
    st.warning("Login required")
    st.stop()

headers = {"Authorization": f"Bearer {st.session_state['token']}"}

name = st.text_input("Item Name")

category_id = st.text_input("Category ID")

description = st.text_area("Description")

if st.button("Create Item"):

    payload = {
        "name": name,
        "category_id": category_id,
        "description": description
    }

    response = requests.post(
        f"{BASE_URL}/items/",
        headers=headers,
        json=payload
    )

    if response.status_code == 200:
        st.success("Item Created Successfully")
        st.json(response.json())
    else:
        st.error(response.text)
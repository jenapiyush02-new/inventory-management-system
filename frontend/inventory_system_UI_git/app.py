import streamlit as st

st.set_page_config(page_title="Inventory System", layout="wide")

st.title("Inventory Management System")

if "token" not in st.session_state:
    st.warning("Please login from Login page.")
    

st.set_page_config(page_title="Inventory System", layout="wide")

st.sidebar.title("Inventory System")

if "role" in st.session_state:
    st.sidebar.write(f"Logged in as: {st.session_state['role']}")
    

if "token" in st.session_state:
    if st.sidebar.button("Logout"):
        st.session_state.clear()
        st.rerun()
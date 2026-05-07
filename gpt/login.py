import streamlit as st
from utils.auth import verify_user
from utils.styling import load_css

def login_page():

    load_css()

    st.title("StemQuant Login")

    user = st.text_input(
    "Username",
    key="login_user"
    )

    pw = st.text_input(
    "Password",
    type="password",
    key="login_pass"
    )

    if st.button("Login"):

        if verify_user(
        user,
        pw
        ):
            st.session_state.authenticated=True
            st.session_state.user=user
            st.rerun()

        else:
            st.error(
            "Invalid credentials"
            )
            def load_style():
                load_css()
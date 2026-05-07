import streamlit as st
from utils.auth import register_user
from utils.styling import load_css

def register_page():

    load_css()

    st.title("Create Account")

    user = st.text_input(
    "Username",
    key="reg_user"
    )

    email = st.text_input(
    "Email",
    key="reg_email"
    )

    pw = st.text_input(
    "Password",
    type="password",
    key="reg_pass"
    )

    if st.button("Register"):

        if register_user(
            user,
            email,
            pw
        ):
            st.success(
            "Registered successfully"
            )
        else:
            st.error(
            "Username exists"
            )
            def load_style():
                load_css()
import streamlit as st
from utils.auth import register_user


def register_page():

    st.markdown("<br>", unsafe_allow_html=True)

    user = st.text_input(
        "Username",
        placeholder="Choose a username",
        key="reg_user"
    )

    email = st.text_input(
        "Email",
        placeholder="your@email.com",
        key="reg_email"
    )

    pw = st.text_input(
        "Password",
        type="password",
        placeholder="Create a strong password",
        key="reg_pass"
    )

    st.markdown("<br>", unsafe_allow_html=True)

    if st.button("Create Account →", use_container_width=True, key="reg_btn"):

        if register_user(user, email, pw):
            st.success("✅  Account created! You can now log in.")
        else:
            st.error("❌  Username already exists. Try another.")

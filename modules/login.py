import streamlit as st
from utils.auth import verify_user


def login_page():

    st.markdown("<br>", unsafe_allow_html=True)

    user = st.text_input(
        "Username",
        placeholder="Enter your username",
        key="login_user"
    )

    pw = st.text_input(
        "Password",
        type="password",
        placeholder="Enter your password",
        key="login_pass"
    )

    st.markdown("<br>", unsafe_allow_html=True)

    if st.button("Login →", use_container_width=True, key="login_btn"):

        if verify_user(user, pw):
            st.session_state.authenticated = True
            st.session_state.user = user
            st.rerun()
        else:
            st.error("❌  Invalid credentials. Please try again.")

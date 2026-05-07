import streamlit as st
import requests
from streamlit_lottie import st_lottie


st.title(
"Lottie Animation Preview"
)


def load_lottie(url):

    r=requests.get(url)

    if r.status_code!=200:
        st.error("Animation not found")
        return None

    return r.json()


url=st.text_input(
"Paste Lottie JSON URL",
"https://assets10.lottiefiles.com/packages/lf20_tfb3estd.json"
)


if st.button("Preview Animation"):

    anim=load_lottie(
    url
    )

    if anim:
        st_lottie(
        anim,
        height=500,
        speed=1,
        key="preview"
        )
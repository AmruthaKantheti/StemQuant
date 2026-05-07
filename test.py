import streamlit as st
import requests
from streamlit_lottie import st_lottie

def load(url):
    return requests.get(url).json()

url=st.text_input(
"https://assets10.lottiefiles.com/packages/lf20_tfb3estd.json"
)

if url:
    st_lottie(
    load(url),
    height=500
    )
import streamlit as st

from modules.login import login_page
from modules.register import register_page
from modules.dashboard import dashboard_page
from utils.styling import load_css


# ── PAGE CONFIG ────────────────────────────────────────
st.set_page_config(
    page_title="StemQuant",
    page_icon="🧬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── GLOBAL STYLING ─────────────────────────────────────
load_css()

# Hide default streamlit chrome
st.markdown("""
<style>
#MainMenu { visibility: hidden; }
footer    { visibility: hidden; }
header    { visibility: hidden; }
[data-testid="stSidebarNav"] { display: none; }
</style>
""", unsafe_allow_html=True)

# ── SESSION STATE ──────────────────────────────────────
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

# ── AUTH PAGES ─────────────────────────────────────────
if not st.session_state.authenticated:

    # Centre the login card
    _, mid, _ = st.columns([1, 1.6, 1])

    with mid:
        st.markdown("""
<div style='text-align:center;padding:48px 0 32px;'>
    <div style='width:64px;height:64px;
                background:linear-gradient(135deg,#6366f1,#a855f7);
                border-radius:20px;
                display:flex;align-items:center;justify-content:center;
                font-size:30px;margin:0 auto 16px;
                box-shadow:0 6px 24px rgba(99,102,241,0.4);'>
        🧬
    </div>
    <h1 style='font-size:36px !important;margin-bottom:6px;'>StemQuant</h1>
    <p style='font-size:14px;color:#64748b;'>Pan-cancer Stemness Prediction Platform</p>
</div>
""", unsafe_allow_html=True)

        st.markdown("<div class='glass-panel'>", unsafe_allow_html=True)

        tab1, tab2 = st.tabs(["  Login  ", "  Register  "])

        with tab1:
            login_page()

        with tab2:
            register_page()

        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown(
            "<div class='sq-footer'>© 2026 StemQuant. All rights reserved.</div>",
            unsafe_allow_html=True
        )

# ── DASHBOARD ──────────────────────────────────────────
else:
    dashboard_page()

import streamlit as st
from modules.prediction import prediction_page
from modules.history import history_page
from modules.about import about_page


def dashboard_page():

    #########################################
    # SIDEBAR NAV
    #########################################

    with st.sidebar:

        st.markdown("""
        ## 🧬 StemQuant
        Pan-cancer Stemness Prediction Platform
        """)

        st.divider()

        page = st.radio(
            "",
            [
                "🏠 Dashboard",
                "🧬 Prediction",
                "ℹ About",
                "📜 History"
            ],
            key="sidebar_nav"
        )

        st.divider()

        if st.button("Logout"):
            st.session_state.authenticated=False
            st.rerun()


    #########################################
    # ROUTING
    #########################################

    if "Prediction" in page:
        prediction_page()
        return

    if "About" in page:
        about_page()
        return

    if "History" in page:
        history_page()
        return



    #########################################
    # DASHBOARD HOME
    #########################################

    st.title("StemQuant Dashboard")

    c1,c2,c3,c4=st.columns(4)

    with c1:
        st.metric(
            "Predictions",
            "128",
            "+12%"
        )

    with c2:
        st.metric(
            "High Stemness",
            "46",
            "+8%"
        )

    with c3:
        st.metric(
            "Avg Stemness",
            "0.62"
        )

    with c4:
        st.metric(
            "Uploads",
            "32",
            "+14%"
        )


    st.divider()


    st.subheader("Quick Prediction")

    st.info(
    "Use Prediction page from left panel to upload samples and run stemness scoring."
    )


    st.divider()

    st.subheader("Recent Predictions")

    st.dataframe(
    {
      "Sample":["BRCA_1","LUAD_2","LGG_4"],
      "Stemness":[0.87,0.45,0.78],
      "Risk":["High","Medium","High"]
    },
    use_container_width=True
    )


    a,b=st.columns(2)

    with a:
        st.info("""
Model Performance

Stemness R²: 0.994
Risk AUC: 0.990
""")

    with b:
        st.success("""
Supported Cancers

LGG
GBM
LIHC
""")
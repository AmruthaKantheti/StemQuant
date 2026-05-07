import streamlit as st
from modules.prediction import prediction_page
from modules.history import history_page
from modules.about import about_page


def dashboard_page():

    #################################################
    # DASHBOARD STYLING
    #################################################

    st.markdown("""
<style>

section[data-testid="stSidebar"]{
background:rgba(255,255,255,.55);
backdrop-filter:blur(22px);
border-right:1px solid rgba(255,255,255,.4);
}

.main .block-container{
padding-top:2rem;
max-width:1250px;
}

.metric-box{
background:rgba(255,255,255,.72);
backdrop-filter:blur(18px);
padding:25px;
border-radius:24px;
box-shadow:0 8px 35px rgba(0,0,0,.06);
}

.hero-box{
background:rgba(255,255,255,.58);
backdrop-filter:blur(22px);
padding:35px;
border-radius:30px;
box-shadow:0 8px 45px rgba(0,0,0,.06);
}

.pred-box{
background:rgba(255,255,255,.62);
padding:30px;
border-radius:30px;
box-shadow:0 8px 45px rgba(0,0,0,.05);
}

.table-box{
background:rgba(255,255,255,.60);
padding:30px;
border-radius:28px;
box-shadow:0 8px 45px rgba(0,0,0,.05);
}

</style>
""",
unsafe_allow_html=True)


    #################################################
    # SIDEBAR
    #################################################

    with st.sidebar:

        st.markdown("## 🧬 StemQuant")
        st.caption("Pan-cancer Stemness Prediction Platform")

        page=st.radio(
        "",
        [
        " Dashboard",
        " Prediction",
        " About",
        " History"
        ]
        )


    #################################################
    # ROUTING
    #################################################

    if "Prediction" in page:
        prediction_page()
        return

    if "About" in page:
        about_page()
        return

    if "History" in page:
        history_page()
        return



    #################################################
    # HERO HEADER
    #################################################

    c1,c2=st.columns([1.3,1])

    with c1:

        st.title(
        "Welcome back, Researcher"
        )

        st.write(
        "Analyze and predict stemness scores with confidence."
        )

    with c2:

        st.markdown("""
<div class='hero-box'>
<h3>Stemness Analytics Platform</h3>
<p>Integrated ML-driven cancer stemness assessment</p>
</div>
""",
unsafe_allow_html=True)



    st.write("")



    #################################################
    # METRICS
    #################################################

    a,b,c,d=st.columns(4)

    with a:
        st.metric(
        "Total Predictions",
        "128",
        "+12%"
        )

    with b:
        st.metric(
        "High Stemness",
        "46",
        "+8%"
        )

    with c:
        st.metric(
        "Avg Stemness",
        "0.62",
        "+5%"
        )

    with d:
        st.metric(
        "Data Uploads",
        "32",
        "+14%"
        )



    st.write("")
    st.write("")



    #################################################
    # QUICK PREDICTION GLASS PANEL
    #################################################

    st.markdown("""
<div class='pred-box'>
<h2>Quick Prediction</h2>
<p>Choose prediction mode and upload your data.</p>
</div>
""",
unsafe_allow_html=True)



    mode=st.radio(
    "Prediction Mode",
    [
    "Full Transcriptome Mode",
    "Marker Panel Mode"
    ],
    horizontal=True
    )


    uploaded=st.file_uploader(
    "Upload CSV File"
    )


    if uploaded is not None:

        st.success(
        "File uploaded successfully"
        )

        if st.button(
        "Run Prediction"
        ):
            prediction_page()



    st.write("")
    st.write("")



    #################################################
    # RECENT PREDICTIONS
    #################################################

    st.markdown("""
<div class='table-box'>
<h2>Recent Predictions</h2>
</div>
""",
unsafe_allow_html=True)



    recent_data={
    "Sample ID":[
    "BRCA_001",
    "LUAD_023",
    "COAD_015",
    "HNSC_007"
    ],

    "Mode":[
    "Full Transcriptome",
    "Marker Panel",
    "Full Transcriptome",
    "Marker Panel"
    ],

    "Stemness Score":[
    0.87,
    0.45,
    0.22,
    0.78
    ],

    "Risk Category":[
    "High",
    "Medium",
    "Low",
    "High"
    ],

    "Date":[
    "2026-04-25",
    "2026-04-25",
    "2026-04-24",
    "2026-04-24"
    ]
    }


    st.dataframe(
    recent_data,
    use_container_width=True
    )



    st.write("")
    st.write("")



    #################################################
    # LOWER PANELS
    #################################################

    x,y=st.columns(2)


    with x:

        st.info("""
Model Performance

• Stemness R² : 0.994

• Risk AUC : 0.990

• Cross-validation stable
""")


    with y:

        st.success("""
Supported Cancers

• LGG

• GBM

• LIHC
""")


    st.write("")
    st.caption(
    "© StemQuant Research Platform"
    )
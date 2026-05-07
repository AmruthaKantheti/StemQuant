import streamlit as st


def about_page():

    st.markdown("<h1>About StemQuant</h1>", unsafe_allow_html=True)
    st.markdown(
        "<p style='font-size:15px;'>Pan-Cancer Stemness Prediction Platform</p>",
        unsafe_allow_html=True
    )

    st.write("")

    c1, c2 = st.columns(2)

    with c1:
        st.markdown("""
<div class='glass-panel'>
    <h3>🔬 Overview</h3>
    <p>StemQuant predicts tumor stemness and prognostic risk using
    state-of-the-art machine learning trained on pan-cancer
    transcriptomic data.</p>
</div>
""", unsafe_allow_html=True)

        st.markdown("""
<div class='glass-panel'>
    <h3>🎯 Core Modules</h3>
    <p>• Full Transcriptome Prediction</p>
    <p>• Marker Panel Prediction</p>
    <p>• Prognostic Risk Scoring</p>
    <p>• Biological Interpretation</p>
</div>
""", unsafe_allow_html=True)

    with c2:
        st.markdown("""
<div class='glass-panel'>
    <h3>🧬 Cancer Types Supported</h3>
    <p>• <strong>LGG</strong> — Lower Grade Glioma</p>
    <p>• <strong>GBM</strong> — Glioblastoma Multiforme</p>
    <p>• <strong>LIHC</strong> — Liver Hepatocellular Carcinoma</p>
</div>
""", unsafe_allow_html=True)

        st.markdown("""
<div class='glass-panel'>
    <h3>⚙️ Methods Used</h3>
    <p>• Elastic Net Regression</p>
    <p>• Random Forest Classifier</p>
    <p>• Cox Survival Modeling</p>
    <p>• Pathway Enrichment Analysis</p>
</div>
""", unsafe_allow_html=True)

    st.write("")

    st.markdown("### 📈 Model Performance")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Stemness Model R²", "0.994", "Elastic Net CV")
    with col2:
        st.metric("Risk Model AUC",    "0.990", "Random Forest")
    with col3:
        st.metric("CV Folds",          "5-Fold", "Stable")

    st.write("")

    st.markdown("""
<div class='glass-panel'>
    <h3>🚀 Applications</h3>
    <p>• Stemness quantification across cancer types</p>
    <p>• Prognostic stratification of tumor samples</p>
    <p>• Biomarker discovery and validation</p>
    <p>• Translational cancer research support</p>
</div>
""", unsafe_allow_html=True)

    st.markdown(
        "<div class='sq-footer'>© 2026 StemQuant. All rights reserved.</div>",
        unsafe_allow_html=True
    )

import streamlit as st


def about_page():

    st.title(
    "About StemQuant"
    )

    st.write(
    "Pan-Cancer Stemness Prediction Platform"
    )

    st.markdown("""
### Overview

StemQuant predicts tumor stemness and
prognostic risk using machine learning.

### Core Modules

• Full Transcriptome Prediction

• Marker Panel Prediction

• Prognostic Risk Scoring

• Biological Interpretation


### Cancer Types Supported

- LGG
- GBM
- LIHC


### Methods Used

- Elastic Net Regression  
- Random Forest  
- Cox Survival Modeling  
- Pathway Enrichment


### Applications

- Stemness quantification  
- Prognostic stratification  
- Biomarker discovery  
- Translational cancer research
""")


    st.subheader(
    "Model Performance"
    )

    c1,c2=st.columns(2)

    with c1:
        st.metric(
        "Stemness Model R²",
        "0.994"
        )

    with c2:
        st.metric(
        "Risk Model AUC",
        "0.99"
        )
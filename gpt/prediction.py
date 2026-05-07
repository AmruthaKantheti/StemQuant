import streamlit as st
import pandas as pd
import numpy as np

from utils.predictor import (
predict_stemness,
predict_marker
)

from utils.db import connect


###################################################
# SAVE HISTORY
###################################################

def save_history(
user,
sample,
score,
cls
):

    conn=connect()
    c=conn.cursor()

    c.execute(
"""
INSERT INTO history
(username,sample_name,prediction,classification)
VALUES (?,?,?,?)
""",
(
user,
sample,
score,
cls
)
)

    conn.commit()
    conn.close()


###################################################
# MAIN PAGE
###################################################

def prediction_page():

    st.title(
    "Stemness Prediction"
    )


    ###################################################
    # MODEL MODE
    ###################################################

    mode=st.radio(
    "Prediction Mode",
    [
    "Full Transcriptome",
    "Marker Panel"
    ]
    )


    ###################################################
    # UPLOAD
    ###################################################

    file=st.file_uploader(
    "Upload expression matrix CSV"
    )

    if file is not None:

        df=pd.read_csv(
        file,
        index_col=0
        )

        st.subheader(
        "Uploaded Data Preview"
        )

        st.dataframe(
        df.head()
        )


        ###################################################
        # FULL MODEL
        ###################################################

        if mode=="Full Transcriptome":

            pred,prob= predict_stemness(
            df
            )


        ###################################################
        # MARKER MODEL
        ###################################################

        else:

            pred = predict_marker(
            df
            )

            pred=np.array(pred)

            norm=pred/pred.max()

            prob=np.column_stack(
            (
            1-norm,
            norm
            )
            )


        ###################################################
        # RESULTS
        ###################################################

        results=pd.DataFrame(
        {
        "Predicted_Stemness":pred,
        "Risk_Probability":prob[:,1]
        },
        index=df.index
        )


        st.subheader(
        "Predictions"
        )

        st.dataframe(
        results
        )


        ###################################################
        # INTERPRET TOP SAMPLE PER CATEGORY
        ###################################################

        st.subheader(
        "Result Interpretation"
        )

        results["Stemness_Class"]="Low"

        results.loc[
        results["Predicted_Stemness"]>=1.8,
        "Stemness_Class"
        ]="Intermediate"

        results.loc[
        results["Predicted_Stemness"]>2.3,
        "Stemness_Class"
        ]="High"


        for category in [
        "High",
        "Intermediate",
        "Low"
        ]:

            subset=results[
            results["Stemness_Class"]==category
            ]

            if len(subset)==0:
                continue


            top=subset.sort_values(
            by="Predicted_Stemness",
            ascending=False
            ).iloc[0]


            sample_id=subset.sort_values(
            by="Predicted_Stemness",
            ascending=False
            ).index[0]


            stemness=top[
            "Predicted_Stemness"
            ]

            risk=top[
            "Risk_Probability"
            ]


            if risk>0.70:
                prog="High Risk"

            elif risk>=0.30:
                prog="Moderate Risk"

            else:
                prog="Low Risk"


            st.markdown(
f"""
## {category} Stemness Representative

Sample:
**{sample_id}**

Stemness Score:
**{stemness:.3f}**

Risk Probability:
**{risk:.3f}**

Prognostic Group:
**{prog}**
"""
)


            if category=="High":

                st.warning(
"""
Strong stem-like aggressive phenotype.

Possible:
• therapy resistance
• poor prognosis
• tumor progression
"""
)

            elif category=="Intermediate":

                st.info(
"""
Intermediate stemness phenotype.

Partial stem-cell programs may be active.
"""
)

            else:

                st.success(
"""
Lower stemness phenotype.

Comparatively less aggressive biology.
"""
)



        ###################################################
        # LEGEND
        ###################################################

        st.subheader(
        "How To Interpret Scores"
        )

        st.info(
"""
Stemness

<1.8 = Low

1.8-2.3 = Intermediate

>2.3 = High


Risk Probability

0-0.30 = Low risk

0.30-0.70 = Moderate risk

>0.70 = High risk
"""
)


        ###################################################
        # BIOLOGICAL NOTE
        ###################################################

        if mode=="Marker Panel":

            st.subheader(
            "Marker Panel Used"
            )

            st.write(
"""
Model uses:

SOX2
NANOG
POU5F1
PROM1
MYC
KLF4
ALDH1A1
CD44
"""
)

        else:

            st.subheader(
            "Biological Meaning"
            )

            st.write(
"""
Predictions generated using
pan-cancer transcriptomic model
trained on GBM, LGG and LIHC.
"""
)


        ###################################################
        # SAVE HISTORY
        ###################################################

        for i,sample in enumerate(
        df.index
        ):

            save_history(
            st.session_state.user,
            str(sample),
            float(prob[i,1]),
            str(pred[i])
            )

        st.success(
        "Predictions saved to user history."
        )
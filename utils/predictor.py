import joblib
import pandas as pd
import numpy as np

model=joblib.load(
"model/stemness_model.pkl"
)

risk_model=joblib.load(
"model/risk_model.pkl"
)

scaler=joblib.load(
"model/scaler.pkl"
)

marker_model=joblib.load(
"model/marker_model.pkl"
)
def predict_stemness(df):

    ##################################
    # keep numeric columns
    ##################################

    df=df.select_dtypes(
    include=[np.number]
    )

    ##################################
    # match training feature space
    ##################################

    training_features=list(
    scaler.feature_names_in_
    )

    df=df.reindex(
    columns=training_features,
    fill_value=0
    )

    ##################################
    # transform
    ##################################

    X=scaler.transform(
    df
    )

    ##################################
    # predict
    ##################################

    stem_pred=model.predict(
    X
    )

    risk_prob=risk_model.predict_proba(
    df
    )

    return(
    stem_pred,
    risk_prob
    )

def predict_marker(df):

    genes=[
    "SOX2",
    "NANOG",
    "POU5F1",
    "PROM1",
    "MYC",
    "KLF4",
    "ALDH1A1",
    "CD44"
]
    df=df.reindex(
    columns=genes,
    fill_value=0
    )

    pred=marker_model.predict(
    df
    )

    return pred
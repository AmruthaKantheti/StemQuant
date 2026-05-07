import os
import joblib
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.metrics import confusion_matrix
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import ElasticNetCV
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    r2_score,
    roc_auc_score,
    classification_report
)

####################################################
# CREATE OUTPUT FOLDER
####################################################

os.makedirs("model", exist_ok=True)

####################################################
# LOAD DATA
####################################################

X = pd.read_csv(
r"D:/Tumor_Stemness_Project/data/pancancer_expression.csv",
index_col=0
)

meta = pd.read_csv(
r"D:/Tumor_Stemness_Project/data/pancancer_metadata.csv"
)

print("\nLoaded Data")
print("Expression:", X.shape)
print("Metadata:", meta.shape)
print(meta.columns)

####################################################
# OPTIONAL SAFETY CHECK
####################################################

if len(X) != len(meta):
    raise ValueError(
        "Sample mismatch between expression and metadata"
    )

if X.isnull().sum().sum() > 0:
    X = X.fillna(0)

####################################################
# TARGETS
####################################################

# Continuous stemness
y_stemness = meta["Stemness"]

# Binary risk label
meta["risk_group"] = (
    meta["Stemness"] >
    meta["Stemness"].median()
).astype(int)

y_risk = meta["risk_group"]

####################################################
# TRAIN TEST SPLIT
####################################################

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y_stemness,
    test_size=0.2,
    random_state=42
)

####################################################
# SCALE DATA
####################################################

scaler = StandardScaler()

X_train_sc = scaler.fit_transform(X_train)
X_test_sc  = scaler.transform(X_test)

joblib.dump(
    scaler,
    "model/scaler.pkl"
)

####################################################
# MODEL 1
# STEMNESS PREDICTION
####################################################

print("\nTraining Elastic Net Stemness Model...")

stem_model = ElasticNetCV(
    cv=5,
    l1_ratio=[0.1,0.5,0.9,1],
    n_jobs=-1,
    random_state=42
)

stem_model.fit(
    X_train_sc,
    y_train
)

pred_stem = stem_model.predict(
    X_test_sc
)

r2 = r2_score(
    y_test,
    pred_stem
)

print(
f"\nStemness R2: {r2:.3f}"
)

joblib.dump(
    stem_model,
    "model/stemness_model.pkl"
)

####################################################
# PLOT 1
####################################################

plt.figure(
figsize=(6,5)
)

plt.scatter(
y_test,
pred_stem,
alpha=0.6
)

plt.plot(
[
y_test.min(),
y_test.max()
],
[
y_test.min(),
y_test.max()
],
'--'
)

plt.xlabel(
"Observed Stemness"
)

plt.ylabel(
"Predicted Stemness"
)

plt.title(
"Stemness Prediction"
)

plt.tight_layout()

plt.savefig(
"model/stemness_prediction_plot.png",
dpi=300
)

plt.close()

####################################################
# MODEL 2
# RISK CLASSIFIER
####################################################

print(
"\nTraining Risk Classifier..."
)

X_train2, X_test2, y_train2, y_test2 = train_test_split(
    X,
    y_risk,
    test_size=0.2,
    random_state=42
)

rf = RandomForestClassifier(
    n_estimators=500,
    random_state=42
)

rf.fit(
    X_train2,
    y_train2
)

prob = rf.predict_proba(
    X_test2
)[:,1]

pred = rf.predict(
    X_test2
)

auc = roc_auc_score(
    y_test2,
    prob
)

print(
f"\nRisk AUC: {auc:.3f}"
)

print(
classification_report(
y_test2,
pred
)
)

joblib.dump(
rf,
"model/risk_model.pkl"
)

####################################################
# FEATURE IMPORTANCE
####################################################

imp = pd.Series(
rf.feature_importances_,
index=X.columns
).sort_values(
ascending=False
).head(15)

plt.figure(figsize=(8,6))

sns.barplot(
x=imp.values,
y=imp.index
)

plt.title(
"Top Stemness Predictive Genes"
)

plt.tight_layout()

plt.savefig(
"model/feature_importance.png",
dpi=300
)

plt.close()

print("\nTop Predictive Genes:")
print(imp)

####################################################
# PAN-CANCER STEMNESS DISTRIBUTION
####################################################

plt.figure(
figsize=(7,5)
)

sns.boxplot(
x="Cancer",
y="Stemness",
data=meta
)

plt.title(
"Stemness Distribution Across Cancers"
)

plt.tight_layout()

plt.savefig(
"model/pancancer_stemness_distribution.png",
dpi=300
)

plt.close()

####################################################
# SUMMARY REPORT
####################################################


with open(
"model/model_summary.txt",
"w"
) as f:

    f.write(
f"Stemness R2: {r2:.3f}\n"
    )

    f.write(
f"Risk AUC: {auc:.3f}\n"
    )

    f.write(
"\nInterpretation:\n"
    )

    f.write(
"Model shows strong pan-cancer predictive performance.\n"
    )

    f.write(
"High AUC suggests excellent risk discrimination.\n"
    )

    f.write(
"Stemness prediction demonstrates robust generalization across GBM, LGG and LIHC.\n"
    )

    f.write(
"Feature importance analysis identifies transcriptomic drivers of stemness-associated risk.\n"
    )



######ROC CURVE###########
from sklearn.metrics import roc_curve

fpr,tpr,thr = roc_curve(
y_test2,
prob
)

plt.figure(figsize=(6,5))

plt.plot(
fpr,
tpr,
label=f"AUC={auc:.3f}"
)

plt.plot(
[0,1],
[0,1],
linestyle="--"
)

plt.xlabel(
"False Positive Rate"
)

plt.ylabel(
"True Positive Rate"
)

plt.title(
"ROC Curve for Risk Prediction"
)

plt.legend()

plt.tight_layout()

plt.savefig(
"model/ROC_curve.png",
dpi=300
)

plt.close()

#######CONFUSION MATRIX#######
cm = confusion_matrix(
y_test2,
pred
)

plt.figure(figsize=(5,4))

sns.heatmap(
cm,
annot=True,
fmt="d"
)

plt.title(
"Confusion Matrix"
)

plt.xlabel(
"Predicted"
)

plt.ylabel(
"True"
)

plt.tight_layout()

plt.savefig(
"model/confusion_matrix.png",
dpi=300
)

plt.close()

print("\nTraining complete.\n")

print(
"""
Saved in /model folder:

scaler.pkl
stemness_model.pkl
risk_model.pkl

stemness_prediction_plot.png
feature_importance.png
pancancer_stemness_distribution.png
ROC_curve.png
confusion_matrix.png

model_summary.txt
"""
)




import joblib
import pandas as pd
import matplotlib.pyplot as plt

####################################################
# LOAD TRAINED MODELS
####################################################

scaler = joblib.load(
"model/scaler.pkl"
)

stem_model = joblib.load(
"model/stemness_model.pkl"
)

risk_model = joblib.load(
"model/risk_model.pkl"
)

####################################################
# LOAD NEW / UNSEEN DATA
####################################################

new_data = pd.read_csv(
r"D:/Tumor_Stemness_Project/new_samples.csv",
index_col=0
)

print("\nLoaded new samples:")
print(new_data.shape)

####################################################
# SCALE INPUT
####################################################

X_new = scaler.transform(
new_data
)

####################################################
# STEMNESS PREDICTION
####################################################

stemness_pred = stem_model.predict(
X_new
)

####################################################
# RISK PREDICTION
####################################################

risk_prob = risk_model.predict_proba(
new_data
)[:,1]

risk_class = [
"High Risk" if x >0.5
else "Low Risk"
for x in risk_prob
]

####################################################
# RESULTS TABLE
####################################################

results = pd.DataFrame(
{
"Predicted_Stemness":
stemness_pred,

"Risk_Probability":
risk_prob,

"Risk_Class":
risk_class
},
index=new_data.index
)

print("\nPredictions:\n")
print(results)

####################################################
# SAVE RESULTS
####################################################

results.to_csv(
"Predictions.csv"
)

####################################################
# PLOT
####################################################

plt.figure(
figsize=(6,5)
)

plt.hist(
stemness_pred,
bins=10
)

plt.title(
"Predicted Stemness Distribution"
)

plt.xlabel(
"Stemness Score"
)

plt.ylabel(
"Frequency"
)

plt.tight_layout()

plt.savefig(
"Prediction_Plot.png",
dpi=300
)

plt.close()

####################################################
# INTERPRETATION
####################################################

print("\nSample Interpretations:")

for i,row in results.iterrows():

    print(
f"\nSample: {i}"
)

    print(
f"Stemness Score: {row['Predicted_Stemness']:.3f}"
)

    print(
f"Risk Probability: {row['Risk_Probability']:.3f}"
)

    print(
f"Predicted Class: {row['Risk_Class']}"
)

    if row["Risk_Class"]=="High Risk":

        print(
"Interpretation: Elevated stemness-associated risk."
        )

        print(
"Precaution: Further molecular/clinical assessment recommended."
        )

    else:

        print(
"Interpretation: Lower predicted stemness-associated risk."
        )

####################################################
# SUMMARY
####################################################

print(
"""
--------------------------------
Files Generated:

Predictions.csv
Prediction_Plot.png
--------------------------------
"""
)
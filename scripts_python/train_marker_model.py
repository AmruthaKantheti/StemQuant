import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor

X=pd.read_csv(
"data/pancancer_expression.csv",
index_col=0
)

meta=pd.read_csv(
"data/pancancer_metadata.csv"
)

marker_genes=[
"SOX2",
"NANOG",
"POU5F1",
"PROM1",
"MYC",
"KLF4",
"ALDH1A1",
"CD44"
]
X=X[marker_genes]

y=meta["Stemness"]

Xtr,Xte,ytr,yte=train_test_split(
X,
y,
test_size=.2,
random_state=42
)

model=RandomForestRegressor(
n_estimators=300
)

model.fit(
Xtr,
ytr
)

joblib.dump(
model,
"model/marker_model.pkl"
)

print("Marker model saved")
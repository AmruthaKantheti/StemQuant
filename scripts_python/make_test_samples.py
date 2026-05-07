import pandas as pd

X = pd.read_csv(
r"D:/Tumor_Stemness_Project/pancancer_expression.csv",
index_col=0
)

# select 5 samples as mock unseen data
new_samples = X.sample(
5,
random_state=42
)

new_samples.to_csv(
r"D:/Tumor_Stemness_Project/new_samples.csv"
)

print("new_samples.csv created")
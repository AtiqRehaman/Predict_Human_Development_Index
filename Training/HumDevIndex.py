import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
import pickle

# 1. Load Dataset
print("--- Step 1: Loading Dataset ---")
Development = pd.read_csv("../Dataset/HDI.csv", encoding="unicode_escape")

# Clean column headers by stripping trailing spaces
Development.columns = Development.columns.str.strip()
print(f"Dataset Loaded. Shape: {Development.shape}\n")

# Define target and specific feature columns based on your exact dataset schema
target_col = "Human Development Index (HDI)"
features_list = [
    'Country', 
    'Life expectancy at birth', 
    'Mean years of schooling', 
    'Gross national income (GNI) per capita'
]

# 2. Exploratory Data Visualization
print("--- Step 2: Generating Diagnostic Visualizations ---")
data1 = Development.head(20)

plt.figure(figsize=(10, 5))
sns.stripplot(x="Mean years of schooling", y=target_col, data=data1)
plt.xticks(rotation=90)
plt.title(f"Mean years of schooling vs {target_col}")
plt.tight_layout()
plt.savefig("schooling_vs_hdi.png")
plt.close()

plt.figure(figsize=(10, 5))
# Create correlation matrix on numeric items only
numeric_data = Development.select_dtypes(include=[np.number])
sns.heatmap(numeric_data.corr(), annot=False, cmap="coolwarm")
plt.title("Correlation Matrix Heatmap")
plt.tight_layout()
plt.savefig("correlation_heatmap.png")
plt.close()
print("Plots saved to disk successfully.\n")

# 3. Feature Selection
# Isolate your independent inputs (X) and target dependent outputs (y)
X = Development[features_list].copy()
y = Development[target_col].copy()

# 4. Handle Missing Values
print("--- Step 3: Handling Missing Values ---")
print("Null values before imputation:\n", X.isnull().sum())

# Replace null values with the mean for your numeric features
numeric_features = ['Life expectancy at birth', 'Mean years of schooling', 'Gross national income (GNI) per capita']

# Clean string numbers or commas in GNI column if they exist, making it numeric
if X['Gross national income (GNI) per capita'].dtype == 'object':
    X['Gross national income (GNI) per capita'] = X['Gross national income (GNI) per capita'].str.replace(',', '').str.strip()
    X['Gross national income (GNI) per capita'] = pd.to_numeric(X['Gross national income (GNI) per capita'], errors='coerce')

for col in numeric_features:
    X[col] = pd.to_numeric(X[col], errors='coerce')
    X[col] = X[col].fillna(X[col].mean())

# If the target target series y has missing items, fill them with its mean
y = pd.to_numeric(y, errors='coerce')
y = y.fillna(y.mean())

print("Null values after imputation:\n", X.isnull().sum(), "\n")

# 5. Categorical Encoding for Country field to map values to string tokens
X["Country"] = X["Country"].astype("category").cat.codes

# 6. Split Data
x_train, x_test, y_train, y_test = train_test_split(X, y, test_size=0.1, random_state=42)

# 7. Model Training
print("--- Step 4: Training Linear Regression Model ---")
reg = LinearRegression()
reg.fit(x_train, y_train)

# Test custom point mapping manually (adjusting indices for 4 features)
sample_test = [[13, 72.0, 5.2, 3341.0]]
print(f"Testing predictive inference with custom data {sample_test}:")
print("Predicted Target output:", reg.predict(sample_test), "\n")

# Evaluate Model Check
y_pred = reg.predict(x_test)
print("Actual Test Values (y_test):", y_test.values[:5])
print("Predicted Test Values (y_pred):", y_pred[:5])
print(f"Model Variance Accuracy (R2 Score): {r2_score(y_test, y_pred):.4f}\n")

# 8. Save Model to Flask directory
print("--- Step 5: Exporting Model File ---")
os.makedirs("../Flask", exist_ok=True)
with open("../Flask/HDI.pkl", "wb") as file:
    pickle.dump(reg, file)
print("Model compiled and exported to ../Flask/HDI.pkl successfully!")

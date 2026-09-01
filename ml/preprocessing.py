from pathlib import Path
import pandas as pd

# ==========================
# Project Paths
# ==========================

BASE_DIR = Path(__file__).resolve().parent.parent
DATASET_DIR = BASE_DIR / "dataset"

# ==========================
# Load Dataset
# ==========================

train = pd.read_csv(DATASET_DIR / "Training.csv")
test = pd.read_csv(DATASET_DIR / "Testing.csv")

# Remove unwanted columns if present
train = train.loc[:, ~train.columns.str.contains("^Unnamed")]
test = test.loc[:, ~test.columns.str.contains("^Unnamed")]

print("=" * 60)
print(" HEALTHCARE AI DATASET INFORMATION")
print("=" * 60)

print(f"\nTraining Shape : {train.shape}")
print(f"Testing Shape  : {test.shape}")

print("\nFirst 10 Columns:")
print(train.columns[:10].tolist())

print("\nLast Column:")
print(train.columns[-1])

print("\nFirst 5 Rows:")
print(train.head())

print("\nMissing Values:")
print(train.isnull().sum().sum())

print("\nDuplicate Rows:")
print(train.duplicated().sum())

print("\nTotal Symptoms :", len(train.columns)-1)
print("Total Diseases :", train.iloc[:, -1].nunique())

print("\nDisease Names:")
print(train.iloc[:, -1].unique())
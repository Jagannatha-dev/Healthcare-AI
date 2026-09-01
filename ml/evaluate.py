from pathlib import Path
import joblib
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
    ConfusionMatrixDisplay
)

from sklearn.model_selection import cross_val_score

# ======================================================
# Project Paths
# ======================================================

BASE_DIR = Path(__file__).resolve().parent.parent

DATASET_DIR = BASE_DIR / "dataset"
MODEL_DIR = BASE_DIR / "ml_model"

# ======================================================
# Load Testing Dataset
# ======================================================

df = pd.read_csv(DATASET_DIR / "Testing.csv")

X = df.drop("prognosis", axis=1)
y = df["prognosis"]

# ======================================================
# Load Encoder and Model
# ======================================================

encoder = joblib.load(MODEL_DIR / "label_encoder.pkl")
model = joblib.load(MODEL_DIR / "model.pkl")

# Encode labels

y_encoded = encoder.transform(y)

# ======================================================
# Prediction
# ======================================================

prediction = model.predict(X)

# ======================================================
# Accuracy
# ======================================================

accuracy = accuracy_score(y_encoded, prediction)

print("=" * 60)
print("MODEL EVALUATION")
print("=" * 60)

print(f"\nAccuracy : {accuracy * 100:.2f}%")

# ======================================================
# Classification Report
# ======================================================

print("\nClassification Report\n")

print(
    classification_report(
        y_encoded,
        prediction,
        target_names=encoder.classes_
    )
)

# ======================================================
# Confusion Matrix
# ======================================================

cm = confusion_matrix(y_encoded, prediction)

fig, ax = plt.subplots(figsize=(15, 15))

disp = ConfusionMatrixDisplay(
    confusion_matrix=cm,
    display_labels=encoder.classes_
)

disp.plot(
    cmap="Blues",
    xticks_rotation=90,
    ax=ax
)

plt.title("Disease Prediction Confusion Matrix")
plt.tight_layout()
plt.show()

# ======================================================
# Feature Importance (Random Forest Only)
# ======================================================

if hasattr(model, "feature_importances_"):

    importance = pd.DataFrame({

        "Symptom": X.columns,

        "Importance": model.feature_importances_

    })

    importance = importance.sort_values(
        by="Importance",
        ascending=False
    )

    print("\nTop 20 Important Symptoms\n")

    print(importance.head(20))

    plt.figure(figsize=(10,8))

    plt.barh(
        importance.head(20)["Symptom"][::-1],
        importance.head(20)["Importance"][::-1]
    )

    plt.xlabel("Importance")
    plt.title("Top 20 Important Symptoms")

    plt.tight_layout()
    plt.show()

print("\nEvaluation Completed Successfully.")
print("=" * 60)
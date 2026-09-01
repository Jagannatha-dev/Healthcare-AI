import os
import joblib
import pandas as pd

from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score, classification_report

# =====================================================
# Load Dataset
# =====================================================

print("=" * 60)
print("Loading Dataset...")
print("=" * 60)

train = pd.read_csv("dataset/Training.csv")
test = pd.read_csv("dataset/Testing.csv")

print("Training Shape :", train.shape)
print("Testing Shape  :", test.shape)

# =====================================================
# Prepare Data
# =====================================================

X_train = train.drop("Disease", axis=1)
y_train = train["Disease"]

X_test = test.drop("Disease", axis=1)
y_test = test["Disease"]

# =====================================================
# Encode Labels
# =====================================================

label_encoder = LabelEncoder()

y_train_encoded = label_encoder.fit_transform(y_train)
y_test_encoded = label_encoder.transform(y_test)

# =====================================================
# Train Random Forest
# =====================================================

print("\nTraining Random Forest Model...\n")

model = RandomForestClassifier(
    n_estimators=500,
    max_depth=None,
    min_samples_split=10,
    min_samples_leaf=5,
    max_features="sqrt",
    random_state=42,
    n_jobs=1
)


model.fit(X_train, y_train_encoded)

print("Training Completed!")

# =====================================================
# Evaluate Model
# =====================================================

predictions = model.predict(X_test)

accuracy = accuracy_score(y_test_encoded, predictions)

print("\n" + "=" * 60)
print("MODEL PERFORMANCE")
print("=" * 60)

print(f"Accuracy : {accuracy*100:.2f}%")

print("\nClassification Report:\n")
print(
    classification_report(
        y_test_encoded,
        predictions,
        target_names=label_encoder.classes_,
        zero_division=0
    )
)

# =====================================================
# Save Model
# =====================================================

os.makedirs("models", exist_ok=True)

joblib.dump(model, "models/disease_model.pkl")
joblib.dump(label_encoder, "models/label_encoder.pkl")
joblib.dump(list(X_train.columns), "models/symptoms.pkl")

print("\nSaved:")
print("models/disease_model.pkl")
print("models/label_encoder.pkl")
print("models/symptoms.pkl")

print("\nProject ML Training Completed Successfully!")
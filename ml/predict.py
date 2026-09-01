import joblib
import numpy as np
import os

# Load trained files
MODEL_PATH = "models/disease_model.pkl"
ENCODER_PATH = "models/label_encoder.pkl"
SYMPTOMS_PATH = "models/symptoms.pkl"

model = joblib.load(MODEL_PATH)
label_encoder = joblib.load(ENCODER_PATH)
symptoms = joblib.load(SYMPTOMS_PATH)
from pathlib import Path
import joblib
import numpy as np


# ============================================================
# BASE DIRECTORY
# ============================================================

# Project root:
# C:\Users\ADNIM\Desktop\Healthcare AI
BASE_DIR = Path(__file__).resolve().parent.parent

# Models directory
MODEL_DIR = BASE_DIR / "models"


# ============================================================
# MODEL FILES
# ============================================================

MODEL_PATH = MODEL_DIR / "disease_model.pkl"
ENCODER_PATH = MODEL_DIR / "label_encoder.pkl"
SYMPTOMS_PATH = MODEL_DIR / "symptoms.pkl"


# ============================================================
# CHECK MODEL FILES
# ============================================================

def check_model_files():

    required_files = {
        "Disease Model": MODEL_PATH,
        "Label Encoder": ENCODER_PATH,
        "Symptoms": SYMPTOMS_PATH
    }

    for name, path in required_files.items():

        if not path.exists():

            raise FileNotFoundError(
                f"{name} file not found:\n{path}"
            )


# ============================================================
# LOAD MODEL FILES
# ============================================================

check_model_files()

print("=" * 70)
print("LOADING HEALTHCARE AI MACHINE LEARNING MODEL")
print("=" * 70)

print(f"Model file   : {MODEL_PATH}")
print(f"Encoder file : {ENCODER_PATH}")
print(f"Symptoms file: {SYMPTOMS_PATH}")


# ------------------------------------------------------------
# Load trained disease model
# ------------------------------------------------------------

try:

    model = joblib.load(
        MODEL_PATH,
        mmap_mode="r"
    )

    print("[OK] Disease model loaded successfully.")

except Exception as e:

    print("[ERROR] Could not load disease model.")
    print(f"Reason: {e}")

    raise


# ------------------------------------------------------------
# Load label encoder
# ------------------------------------------------------------

try:

    label_encoder = joblib.load(
        ENCODER_PATH
    )

    print("[OK] Label encoder loaded successfully.")

except Exception as e:

    print("[ERROR] Could not load label encoder.")
    print(f"Reason: {e}")

    raise


# ------------------------------------------------------------
# Load symptoms
# ------------------------------------------------------------

try:

    symptoms = joblib.load(
        SYMPTOMS_PATH
    )

    print("[OK] Symptoms list loaded successfully.")

except Exception as e:

    print("[ERROR] Could not load symptoms file.")
    print(f"Reason: {e}")

    raise


# ============================================================
# NORMALIZE SYMPTOMS
# ============================================================

# Make sure symptoms is a normal Python list.

if isinstance(symptoms, np.ndarray):

    symptoms = symptoms.tolist()

else:

    symptoms = list(symptoms)


# Remove duplicates while maintaining order

symptoms = list(dict.fromkeys(symptoms))


print(f"[OK] Total symptoms: {len(symptoms)}")
print(f"[OK] Total diseases: {len(label_encoder.classes_)}")

print("=" * 70)
print("MACHINE LEARNING MODEL READY")
print("=" * 70)


# ============================================================
# PREDICT DISEASE
# ============================================================

def predict_disease(selected_symptoms):

    """
    Predict disease from selected symptoms.

    Parameters
    ----------
    selected_symptoms : list
        Symptoms selected by the user.

    Returns
    -------
    predicted_disease : str
    confidence : float
    top5_predictions : list
    """

    # --------------------------------------------------------
    # Validate input
    # --------------------------------------------------------

    if not selected_symptoms:

        raise ValueError(
            "No symptoms were selected."
        )


    # --------------------------------------------------------
    # Clean selected symptoms
    # --------------------------------------------------------

    cleaned_symptoms = []

    for symptom in selected_symptoms:

        if symptom is None:
            continue

        symptom = str(symptom).strip()

        if not symptom:
            continue

        cleaned_symptoms.append(symptom)


    if not cleaned_symptoms:

        raise ValueError(
            "No valid symptoms were selected."
        )


    # --------------------------------------------------------
    # Create input vector
    # --------------------------------------------------------

    data = np.zeros(
        len(symptoms),
        dtype=np.float32
    )


    # --------------------------------------------------------
    # Set selected symptoms to 1
    # --------------------------------------------------------

    matched_symptoms = []
    unmatched_symptoms = []

    for symptom in cleaned_symptoms:

        if symptom in symptoms:

            index = symptoms.index(symptom)

            data[index] = 1

            matched_symptoms.append(symptom)

        else:

            unmatched_symptoms.append(symptom)


    # --------------------------------------------------------
    # Make sure at least one symptom matched
    # --------------------------------------------------------

    if not matched_symptoms:

        raise ValueError(
            "None of the selected symptoms were found "
            "in the trained model's symptom list."
        )


    # --------------------------------------------------------
    # Model prediction
    # --------------------------------------------------------

    probabilities = model.predict_proba(
        [data]
    )[0]


    # --------------------------------------------------------
    # Find best prediction
    # --------------------------------------------------------

    best_index = int(
        np.argmax(probabilities)
    )


    predicted_disease = (
        label_encoder
        .inverse_transform([best_index])[0]
    )


    confidence = round(
        float(probabilities[best_index]) * 100,
        2
    )


    # ========================================================
    # TOP 5 PREDICTIONS
    # ========================================================

    top_n = min(
        5,
        len(probabilities)
    )


    top5_indices = (
        np.argsort(probabilities)[-top_n:][::-1]
    )


    top5_predictions = []


    for index in top5_indices:

        index = int(index)

        disease_name = (
            label_encoder
            .inverse_transform([index])[0]
        )

        disease_confidence = round(
            float(probabilities[index]) * 100,
            2
        )


        top5_predictions.append({

            "disease": disease_name,

            "confidence": disease_confidence

        })


    # ========================================================
    # DEBUG INFORMATION
    # ========================================================

    print()
    print("=" * 70)
    print("DISEASE PREDICTION")
    print("=" * 70)

    print(
        f"Selected symptoms : {cleaned_symptoms}"
    )

    print(
        f"Matched symptoms  : {matched_symptoms}"
    )

    if unmatched_symptoms:

        print(
            f"Unmatched symptoms: {unmatched_symptoms}"
        )

    print(
        f"Predicted disease : {predicted_disease}"
    )

    print(
        f"Confidence        : {confidence:.2f}%"
    )

    print()
    print("Top 5 Predictions")
    print("-" * 50)

    for item in top5_predictions:

        print(
            f"{item['disease']:<35}"
            f"{item['confidence']:.2f}%"
        )

    print("=" * 70)


    # ========================================================
    # RETURN
    # ========================================================

    return (
        predicted_disease,
        confidence,
        top5_predictions
    )


# ============================================================
# TEST MODEL DIRECTLY
# ============================================================

if __name__ == "__main__":

    print()
    print("=" * 70)
    print("TESTING DISEASE PREDICTION")
    print("=" * 70)


    sample_symptoms = [

        "itching",

        "skin_rash",

        "nodal_skin_eruptions"

    ]


    try:

        disease, confidence, predictions = (
            predict_disease(
                sample_symptoms
            )
        )


        print()
        print(
            f"Predicted Disease : {disease}"
        )

        print(
            f"Confidence        : "
            f"{confidence:.2f}%"
        )


        print()
        print("Top 5 Predictions")
        print("-" * 50)


        for item in predictions:

            print(
                f"{item['disease']:<35}"
                f"{item['confidence']:.2f}%"
            )


    except Exception as e:

        print()
        print("[ERROR] Prediction test failed.")
        print(f"Reason: {e}")

def predict_disease(selected_symptoms):
    """
    Predict disease from selected symptoms.

    Returns:
        predicted_disease
        confidence
        top5_predictions
    """

    # Create input vector
    data = np.zeros(len(symptoms))

    for symptom in selected_symptoms:
        if symptom in symptoms:
            index = symptoms.index(symptom)
            data[index] = 1

    # Prediction
    probabilities = model.predict_proba([data])[0]

    best_index = np.argmax(probabilities)

    predicted_disease = label_encoder.inverse_transform([best_index])[0]

    confidence = round(probabilities[best_index] * 100, 2)

    # Top 5 predictions
    top5_indices = probabilities.argsort()[-5:][::-1]

    top5_predictions = []

    for i in top5_indices:
        top5_predictions.append({
            "disease": label_encoder.inverse_transform([i])[0],
            "confidence": round(probabilities[i] * 100, 2)
        })

    return predicted_disease, confidence, top5_predictions


# Test
if __name__ == "__main__":

    sample_symptoms = [
        "itching",
        "skin_rash",
        "nodal_skin_eruptions"
    ]

    disease, confidence, predictions = predict_disease(sample_symptoms)

    print(f"\nPredicted Disease : {disease}")
    print(f"Confidence        : {confidence:.2f}%")

    print("\nTop 5 Predictions")
    print("-" * 40)

    for item in predictions:
        print(f"{item['disease']:<35} {item['confidence']}%")
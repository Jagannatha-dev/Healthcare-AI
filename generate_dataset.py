import random
import pandas as pd
from sklearn.model_selection import train_test_split

from dataset.disease_mapping import DISEASE_MAPPING
from dataset.symptoms_master import SYMPTOMS

# ==========================================================
# CONFIGURATION
# ==========================================================

SAMPLES_PER_DISEASE = 600

PRIMARY_PROBABILITY = 0.95
COMMON_PROBABILITY = 0.75
RARE_PROBABILITY = 0.25
NOISE_PROBABILITY = 0.03

random.seed(42)


# ==========================================================
# GENERATE ONE SYNTHETIC PATIENT
# ==========================================================

def generate_patient(disease_name, disease_info):

    patient = {symptom: 0 for symptom in SYMPTOMS}

    # Primary symptoms
    for symptom in disease_info.get("primary", []):
        if symptom in patient:
            if random.random() < PRIMARY_PROBABILITY:
                patient[symptom] = 1

    # Common symptoms
    for symptom in disease_info.get("common", []):
        if symptom in patient:
            if random.random() < COMMON_PROBABILITY:
                patient[symptom] = 1

    # Rare symptoms
    for symptom in disease_info.get("rare", []):
        if symptom in patient:
            if random.random() < RARE_PROBABILITY:
                patient[symptom] = 1

    # Known symptoms of disease
    disease_symptoms = set(
        disease_info.get("primary", [])
        + disease_info.get("common", [])
        + disease_info.get("rare", [])
    )

    # Add random noise symptoms
    for symptom in SYMPTOMS:

        if symptom not in disease_symptoms:

            if random.random() < NOISE_PROBABILITY:
                patient[symptom] = 1

    patient["Disease"] = disease_name

    return patient


# ==========================================================
# BUILD COMPLETE DATASET
# ==========================================================

def build_dataset():

    records = []

    print("=" * 70)
    print("Generating Synthetic Dataset")
    print("=" * 70)

    total = len(DISEASE_MAPPING)

    print(f"Total Diseases : {total}")
    print(f"Samples/Disease: {SAMPLES_PER_DISEASE}")
    print()

    for index, (disease_name, disease_info) in enumerate(DISEASE_MAPPING.items(), start=1):

        print(f"[{index}/{total}] {disease_name}")

        for _ in range(SAMPLES_PER_DISEASE):

            patient = generate_patient(
                disease_name,
                disease_info
            )

            records.append(patient)

    print("\nCreating DataFrame...")

    df = pd.DataFrame(records)

    print("Done.")

    return df


# ==========================================================
# SAVE DATASET
# ==========================================================

def save_dataset(df):

    train_df, test_df = train_test_split(
        df,
        test_size=0.20,
        random_state=42,
        stratify=df["Disease"]
    )

    train_df.to_csv(
        "dataset/Training.csv",
        index=False
    )

    test_df.to_csv(
        "dataset/Testing.csv",
        index=False
    )

    print("\n" + "=" * 70)
    print("Dataset Generated Successfully")
    print("=" * 70)

    print(f"Training Samples : {len(train_df)}")
    print(f"Testing Samples  : {len(test_df)}")
    print(f"Total Samples    : {len(df)}")

    print("\nSaved Files")
    print("dataset/Training.csv")
    print("dataset/Testing.csv")


# ==========================================================
# MAIN
# ==========================================================

if __name__ == "__main__":

    dataset = build_dataset()

    save_dataset(dataset)

    print("\nCompleted Successfully.")
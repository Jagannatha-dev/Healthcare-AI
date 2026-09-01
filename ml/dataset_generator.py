from pathlib import Path
import random
import pandas as pd

# ==========================================================
# CONFIGURATION
# ==========================================================

PATIENTS_PER_DISEASE = 100      # New synthetic patients per disease
REMOVE_PROBABILITY = 0.05       # Probability of removing an existing symptom
ADD_PROBABILITY = 0.40          # Probability of adding another valid symptom
MAX_ADDED_SYMPTOMS = 3          # Maximum symptoms to add

RANDOM_SEED = 42
random.seed(RANDOM_SEED)

# ==========================================================
# PATHS
# ==========================================================

BASE_DIR = Path(__file__).resolve().parent.parent

DATASET_DIR = BASE_DIR / "dataset"

TRAIN_FILE = DATASET_DIR / "Training.csv"

OUTPUT_FILE = DATASET_DIR / "Training_Expanded.csv"

# ==========================================================
# LOAD DATASET
# ==========================================================

print("=" * 60)
print("Loading Dataset...")
print("=" * 60)

df = pd.read_csv(TRAIN_FILE)

SYMPTOM_COLUMNS = list(df.columns[:-1])

print("Symptoms :", len(SYMPTOM_COLUMNS))
print("Diseases :", df["prognosis"].nunique())
print("Rows     :", len(df))

# ==========================================================
# BUILD DISEASE → SYMPTOM MAPPING
# ==========================================================

print("\nBuilding Disease-Symptom Mapping...")

disease_symptoms = {}

for disease in df["prognosis"].unique():

    disease_rows = df[df["prognosis"] == disease]

    symptom_pool = []

    for symptom in SYMPTOM_COLUMNS:

        if disease_rows[symptom].sum() > 0:
            symptom_pool.append(symptom)

    disease_symptoms[disease] = symptom_pool

print("Mapping Created Successfully.")

# ==========================================================
# DATA AUGMENTATION
# ==========================================================

print("\nGenerating Synthetic Patients...")

expanded_rows = []

for disease in df["prognosis"].unique():

    disease_rows = df[df["prognosis"] == disease]

    symptom_pool = disease_symptoms[disease]

    # ------------------------------------------------------
    # Keep Original Patients
    # ------------------------------------------------------

    for _, row in disease_rows.iterrows():
        expanded_rows.append(row.to_dict())

    # ------------------------------------------------------
    # Generate New Patients
    # ------------------------------------------------------

    for _ in range(PATIENTS_PER_DISEASE):

        base_patient = disease_rows.sample(1).iloc[0].copy()

        new_patient = base_patient.copy()

        # ----------------------------------------------
        # Remove some symptoms
        # ----------------------------------------------

        for symptom in symptom_pool:

            if new_patient[symptom] == 1:

                if random.random() < REMOVE_PROBABILITY:

                    new_patient[symptom] = 0

        # ----------------------------------------------
        # Add disease-related symptoms only
        # ----------------------------------------------

        if len(symptom_pool) > 0:

            selected = random.sample(
                symptom_pool,
                min(MAX_ADDED_SYMPTOMS, len(symptom_pool))
            )

            for symptom in selected:

                if new_patient[symptom] == 0:

                    if random.random() < ADD_PROBABILITY:

                        new_patient[symptom] = 1

        new_patient["prognosis"] = disease

        expanded_rows.append(new_patient.to_dict())

print("Synthetic Patients Generated Successfully.")

# ==========================================================
# CREATE DATAFRAME
# ==========================================================

expanded_df = pd.DataFrame(expanded_rows)

# ==========================================================
# REMOVE DUPLICATES
# ==========================================================

before = len(expanded_df)

expanded_df = expanded_df.drop_duplicates()

after = len(expanded_df)

print("\nDuplicates Removed :", before - after)

# ==========================================================
# SHUFFLE DATASET
# ==========================================================

expanded_df = expanded_df.sample(
    frac=1,
    random_state=RANDOM_SEED
).reset_index(drop=True)

# ==========================================================
# SAVE DATASET
# ==========================================================

expanded_df.to_csv(OUTPUT_FILE, index=False)

# ==========================================================
# SUMMARY
# ==========================================================

print("\n" + "=" * 60)
print("TRAINING DATASET GENERATED SUCCESSFULLY")
print("=" * 60)

print("Original Rows     :", len(df))
print("Expanded Rows     :", len(expanded_df))
print("Diseases          :", expanded_df["prognosis"].nunique())
print("Symptoms          :", len(SYMPTOM_COLUMNS))
print("Saved File        :", OUTPUT_FILE)

print("=" * 60)
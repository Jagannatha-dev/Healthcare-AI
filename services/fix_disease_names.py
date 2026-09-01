from pathlib import Path
import pandas as pd
import shutil
from datetime import datetime


# ==========================================================
# Healthcare AI
# CSV Disease Name Migration
# ==========================================================
#
# PURPOSE:
# Change disease names inside ALL medical CSV files so that
# they match the exact names used in DISEASE_MAPPING.
#
# Example:
#
# Diabetes
#      ↓
# Diabetes Mellitus
#
# AIDS
#      ↓
# HIV/AIDS
#
# PCOS
#      ↓
# Polycystic Ovary Syndrome (PCOS)
#
# ==========================================================


# ==========================================================
# PROJECT DIRECTORY
# ==========================================================

BASE_DIR = Path(__file__).resolve().parent

DATASET_DIR = BASE_DIR / "dataset"


# ==========================================================
# BACKUP DIRECTORY
# ==========================================================

BACKUP_DIR = DATASET_DIR / "backup_before_disease_name_fix"

BACKUP_DIR.mkdir(
    exist_ok=True
)


# ==========================================================
# CSV FILES TO MODIFY
# ==========================================================

CSV_FILES = [

    "symptom_description.csv",
    "symptom_precaution.csv",
    "diet.csv",
    "exercise.csv",
    "medicine.csv",
    "doctor_specialist.csv",
    "health_tips.csv",

    "disease_causes.csv",
    "disease_diagnosis.csv",
    "disease_lab_tests.csv",
    "disease_risk_factors.csv",
    "disease_complications.csv",
    "disease_prevention.csv",
    "disease_treatment.csv",
    "disease_severity.csv"

]


# ==========================================================
# DISEASE NAME CONVERSION
#
# LEFT  = CURRENT CSV NAME
# RIGHT = EXACT DISEASE_MAPPING NAME
# ==========================================================

DISEASE_NAME_MAP = {

    # ======================================================
    # Diabetes
    # ======================================================

    "Diabetes":
        "Diabetes Mellitus",

    "diabetes":
        "Diabetes Mellitus",


    # ======================================================
    # Infectious Diseases
    # ======================================================

    "AIDS":
        "HIV/AIDS",

    "Aids":
        "HIV/AIDS",

    "COVID-19":
        "COVID-19",

    "Typhoid":
        "Typhoid",

    "Dengue":
        "Dengue",

    "Malaria":
        "Malaria",

    "Tuberculosis":
        "Tuberculosis",

    "Cholera":
        "Cholera",

    "Influenza":
        "Influenza",


    # ======================================================
    # Liver
    # ======================================================

    "Liver Cirrhosis":
        "Chronic Liver Disease (Cirrhosis)",

    "Alcoholic hepatitis":
        "Alcoholic Liver Disease",

    "Alcoholic Hepatitis":
        "Alcoholic Liver Disease",

    "Fatty Liver Disease":
        "Fatty Liver Disease",

    "Non-Alcoholic Fatty Liver Disease (NAFLD)":
        "Non-Alcoholic Fatty Liver Disease (NAFLD)",

    "Hepatitis A":
        "Hepatitis A",

    "Hepatitis B":
        "Hepatitis B",

    "Hepatitis C":
        "Hepatitis C",

    "Hepatitis D":
        "Hepatitis D",

    "Hepatitis E":
        "Hepatitis E",


    # ======================================================
    # Respiratory
    # ======================================================

    "Asthma":
        "Asthma",

    "Bronchial Asthma":
        "Asthma",

    "COPD":
        "COPD",

    "Pneumonia":
        "Pneumonia",

    "Tuberculosis":
        "Tuberculosis",

    "Sinusitis":
        "Acute Sinusitis",

    "Acute Sinusitis":
        "Acute Sinusitis",

    "Chronic Sinusitis":
        "Chronic Sinusitis",


    # ======================================================
    # Gastrointestinal
    # ======================================================

    "Gastritis":
        "Gastritis",

    "GERD":
        "GERD",

    "Gastroesophageal Reflux Disease (GERD)":
        "GERD",

    "Peptic ulcer disease":
        "Peptic Ulcer Disease",

    "Peptic Ulcer Disease":
        "Peptic Ulcer Disease",

    "Irritable Bowel Syndrome":
        "Irritable Bowel Syndrome (IBS)",

    "Irritable Bowel Syndrome (IBS)":
        "Irritable Bowel Syndrome (IBS)",

    "Ulcerative Colitis":
        "Ulcerative Colitis",

    "Appendicitis":
        "Appendicitis",

    "Gallstones":
        "Gallstones (Cholelithiasis)",

    "Acute Cholecystitis":
        "Acute Cholecystitis",


    # ======================================================
    # Pancreas
    # ======================================================

    "Pancreatitis":
        "Acute Pancreatitis",

    "Acute Pancreatitis":
        "Acute Pancreatitis",

    "Chronic Pancreatitis":
        "Chronic Pancreatitis",


    # ======================================================
    # Kidney / Urinary
    # ======================================================

    "Kidney Stones":
        "Kidney Stones",

    "Urinary Tract Infection":
        "Urinary Tract Infection",


    # ======================================================
    # Neurological
    # ======================================================

    "Parkinson's Disease":
        "Parkinson's Disease",

    "Multiple Sclerosis":
        "Multiple Sclerosis",

    "Epilepsy":
        "Epilepsy",

    "Stroke":
        "Stroke",

    "Migraine":
        "Migraine",


    # ======================================================
    # Musculoskeletal
    # ======================================================

    "Osteoarthritis":
        "Osteoarthritis",

    "Rheumatoid Arthritis":
        "Rheumatoid Arthritis",

    "Osteoporosis":
        "Osteoporosis",

    "Gout":
        "Gout",

    "Fibromyalgia":
        "Fibromyalgia",


    # ======================================================
    # Skin
    # ======================================================

    "Acne":
        "Acne Vulgaris",

    "Acne Vulgaris":
        "Acne Vulgaris",

    "Eczema":
        "Eczema (Atopic Dermatitis)",

    "Eczema (Atopic Dermatitis)":
        "Eczema (Atopic Dermatitis)",

    "Fungal infection":
        "Fungal Infection",

    "Fungal Infection":
        "Fungal Infection",

    "Psoriasis":
        "Psoriasis",

    "Cellulitis":
        "Cellulitis",


    # ======================================================
    # Eye
    # ======================================================

    "Conjunctivitis":
        "Conjunctivitis",

    "Glaucoma":
        "Glaucoma",

    "Cataract":
        "Cataract",


    # ======================================================
    # ENT
    # ======================================================

    "Allergic Rhinitis":
        "Allergic Rhinitis",

    "Tonsillitis":
        "Tonsillitis",

    "Otitis Media":
        "Otitis Media",


    # ======================================================
    # Cardiovascular
    # ======================================================

    "Hypertension":
        "Hypertension",

    "Heart attack":
        "Coronary Artery Disease (CAD)",

    "Coronary Artery Disease (CAD)":
        "Coronary Artery Disease (CAD)",

    "Heart Failure":
        "Heart Failure",

    "Arrhythmia":
        "Arrhythmia",

    "Deep Vein Thrombosis (DVT)":
        "Deep Vein Thrombosis (DVT)",

    "Peripheral Artery Disease (PAD)":
        "Peripheral Artery Disease (PAD)",


    # ======================================================
    # Metabolic
    # ======================================================

    "Obesity":
        "Obesity",

    "Hypoglycemia":
        "Hypoglycemia",

    "Hypothyroidism":
        "Hypothyroidism",

    "Hyperthyroidism":
        "Hyperthyroidism",

    "Hyperlipidemia":
        "Hyperlipidemia",

    "Metabolic Syndrome":
        "Metabolic Syndrome",


    # ======================================================
    # Blood Disorders
    # ======================================================

    "Anemia":
        "Iron Deficiency Anemia",

    "Iron Deficiency Anemia":
        "Iron Deficiency Anemia",

    "Vitamin B12 Deficiency Anemia":
        "Vitamin B12 Deficiency Anemia",

    "Sickle Cell Disease":
        "Sickle Cell Disease",

    "Thalassemia":
        "Thalassemia",

    "Hemophilia":
        "Hemophilia",


    # ======================================================
    # Cancer
    # ======================================================

    "Breast Cancer":
        "Breast Cancer",

    "Cervical Cancer":
        "Cervical Cancer",

    "Colon Cancer":
        "Colon Cancer",

    "Prostate Cancer":
        "Prostate Cancer",

    "Leukemia":
        "Leukemia",

    "Lymphoma":
        "Lymphoma",

    "Skin Cancer":
        "Skin Cancer",

    "Lung Cancer":
        "Lung Cancer",

    "Thyroid Cancer":
        "Thyroid Cancer",

    "Liver Cancer (Hepatocellular Carcinoma)":
        "Liver Cancer (Hepatocellular Carcinoma)",


    # ======================================================
    # Mental Health
    # ======================================================

    "Major Depressive Disorder":
        "Major Depressive Disorder",

    "Generalized Anxiety Disorder":
        "Generalized Anxiety Disorder",

    "Bipolar Disorder":
        "Bipolar Disorder",

    "Schizophrenia":
        "Schizophrenia",

    "Obsessive Compulsive Disorder (OCD)":
        "Obsessive Compulsive Disorder (OCD)",


    # ======================================================
    # Sleep
    # ======================================================

    "Sleep Apnea":
        "Sleep Apnea",

    "Insomnia":
        "Insomnia",

    "Chronic Fatigue Syndrome":
        "Chronic Fatigue Syndrome",


    # ======================================================
    # Women's Health
    # ======================================================

    "PCOS":
        "Polycystic Ovary Syndrome (PCOS)",

    "Polycystic Ovary Syndrome":
        "Polycystic Ovary Syndrome (PCOS)",

    "Endometriosis":
        "Endometriosis",

    "Cervical Cancer":
        "Cervical Cancer",


    # ======================================================
    # Autoimmune
    # ======================================================

    "Systemic Lupus Erythematosus (SLE)":
        "Systemic Lupus Erythematosus (SLE)",

    "Rheumatic Fever":
        "Rheumatic Fever",

}


# ==========================================================
# NORMALIZE TEXT FOR COMPARISON
# ==========================================================

def normalize_text(value):

    if pd.isna(value):
        return ""

    return (
        str(value)
        .strip()
        .lower()
    )


# ==========================================================
# CREATE CASE-INSENSITIVE MAP
# ==========================================================

NORMALIZED_MAP = {

    normalize_text(old_name):
        new_name

    for old_name, new_name
    in DISEASE_NAME_MAP.items()

}


# ==========================================================
# PROCESS ONE CSV
# ==========================================================

def process_csv(filename):

    csv_path = DATASET_DIR / filename

    print()
    print("=" * 70)
    print(f"Processing: {filename}")
    print("=" * 70)

    # ------------------------------------------------------
    # Check file
    # ------------------------------------------------------

    if not csv_path.exists():

        print(
            f"❌ File not found: {csv_path}"
        )

        return

    # ------------------------------------------------------
    # Read CSV
    # ------------------------------------------------------

    try:

        df = pd.read_csv(
            csv_path
        )

    except Exception as e:

        print(
            f"❌ Could not read CSV: {e}"
        )

        return

    # ------------------------------------------------------
    # Check Disease column
    # ------------------------------------------------------

    if "Disease" not in df.columns:

        print(
            "⚠️ No 'Disease' column. Skipping."
        )

        return

    # ------------------------------------------------------
    # Backup
    # ------------------------------------------------------

    backup_path = (
        BACKUP_DIR /
        filename
    )

    shutil.copy2(
        csv_path,
        backup_path
    )

    print(
        f"📦 Backup created: {backup_path}"
    )

    # ------------------------------------------------------
    # Statistics
    # ------------------------------------------------------

    changed = 0
    unchanged = 0
    unknown = set()

    # ------------------------------------------------------
    # Replace Disease Names
    # ------------------------------------------------------

    new_values = []

    for disease in df["Disease"]:

        original = str(disease).strip()

        key = normalize_text(
            original
        )

        if key in NORMALIZED_MAP:

            new_name = NORMALIZED_MAP[key]

            if original != new_name:

                changed += 1

            else:

                unchanged += 1

            new_values.append(
                new_name
            )

        else:

            # Already possibly correct

            unchanged += 1

            new_values.append(
                original
            )

            unknown.add(
                original
            )

    # ------------------------------------------------------
    # Update DataFrame
    # ------------------------------------------------------

    df["Disease"] = new_values

    # ------------------------------------------------------
    # Remove exact duplicate rows
    # ------------------------------------------------------

    before = len(df)

    df = df.drop_duplicates()

    removed_duplicates = (
        before - len(df)
    )

    # ------------------------------------------------------
    # Save
    # ------------------------------------------------------

    try:

        df.to_csv(
            csv_path,
            index=False
        )

    except Exception as e:

        print(
            f"❌ Could not save CSV: {e}"
        )

        return

    # ------------------------------------------------------
    # Result
    # ------------------------------------------------------

    print()
    print(
        f"✅ Changed names    : {changed}"
    )

    print(
        f"ℹ️ Already matching  : {unchanged}"
    )

    print(
        f"🗑️ Duplicate rows    : {removed_duplicates}"
    )

    if unknown:

        print()
        print(
            "⚠️ Names not found in conversion map:"
        )

        for name in sorted(unknown):

            print(
                f"   - {name}"
            )

    print(
        f"💾 Saved: {csv_path}"
    )


# ==========================================================
# MAIN
# ==========================================================

def main():

    print()
    print("=" * 70)
    print("HEALTHCARE AI - DISEASE NAME MIGRATION")
    print("=" * 70)

    print(
        f"Dataset directory:\n{DATASET_DIR}"
    )

    print(
        f"Backup directory:\n{BACKUP_DIR}"
    )

    print()
    print(
        "⚠️ Original CSV files will be backed up before modification."
    )

    input(
        "\nPress ENTER to start..."
    )

    # ======================================================
    # Process Files
    # ======================================================

    for filename in CSV_FILES:

        process_csv(
            filename
        )

    # ======================================================
    # Finished
    # ======================================================

    print()
    print("=" * 70)
    print("✅ DISEASE NAME MIGRATION COMPLETED")
    print("=" * 70)

    print()
    print(
        "Your original CSV files are backed up here:"
    )

    print(
        BACKUP_DIR
    )

    print()
    print(
        "Restart Flask after this operation."
    )


# ==========================================================
# RUN
# ==========================================================

if __name__ == "__main__":

    main()
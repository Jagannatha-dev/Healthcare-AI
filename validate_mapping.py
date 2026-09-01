from dataset.symptoms_master import SYMPTOMS
from dataset.disease_mapping import DISEASE_MAPPING

MASTER = set(SYMPTOMS)

print("=" * 70)
print("VALIDATING DISEASE MAPPING")
print("=" * 70)

errors = 0

for disease, info in DISEASE_MAPPING.items():

    print(f"\nChecking: {disease}")

    used = set()

    for section in ["primary", "common", "rare"]:

        if section not in info:
            print(f"  Missing section: {section}")
            errors += 1
            continue

        for symptom in info[section]:

            if symptom not in MASTER:
                print(f"  Invalid symptom: {symptom}")
                errors += 1

            if symptom in used:
                print(f"  Duplicate symptom: {symptom}")
                errors += 1

            used.add(symptom)

print("\n" + "=" * 70)

if errors == 0:
    print("✓ ALL DISEASES ARE VALID")
else:
    print(f"Found {errors} issue(s).")

print("=" * 70)
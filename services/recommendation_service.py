# ==========================================================
# Healthcare AI - Recommendation Service
# ==========================================================

from pathlib import Path
import re
import pandas as pd


class RecommendationService:

    # ======================================================
    # INITIALIZATION
    # ======================================================

    def __init__(self):

        # --------------------------------------------------
        # Project directory
        # --------------------------------------------------

        base_dir = (
            Path(__file__)
            .resolve()
            .parent
            .parent
        )

        self.dataset = base_dir / "dataset"

        print("\n" + "=" * 70)
        print("INITIALIZING RECOMMENDATION SERVICE")
        print("=" * 70)

        print("Dataset folder:", self.dataset)

        # ==================================================
        # LOAD DATASETS
        # ==================================================

        # Symptom description
        self.symptom_description = self.load_csv(
            "symptom_description.csv"
        )

        # Disease precautions
        self.precaution = self.load_csv(
            "symptom_precaution.csv"
        )

        # Disease datasets
        self.diet = self.load_csv("diet.csv")
        self.exercise = self.load_csv("exercise.csv")
        self.medicine = self.load_csv("medicine.csv")
        self.specialist = self.load_csv("doctor_specialist.csv")
        self.health_tip = self.load_csv("health_tips.csv")

        # IMPORTANT:
        # disease_causes.csv has:
        # Disease, Description
        #
        # Therefore this dataset is used for
        # disease description AND cause information.
        self.disease_description = self.load_csv(
            "disease_causes.csv"
        )

        self.diagnosis = self.load_csv(
            "disease_diagnosis.csv"
        )

        self.lab_tests = self.load_csv(
            "disease_lab_tests.csv"
        )

        self.risk_factors = self.load_csv(
            "disease_risk_factors.csv"
        )

        self.complications = self.load_csv(
            "disease_complications.csv"
        )

        self.prevention = self.load_csv(
            "disease_prevention.csv"
        )

        self.treatment = self.load_csv(
            "disease_treatment.csv"
        )

        self.severity = self.load_csv(
            "disease_severity.csv"
        )

        self.emergency = self.load_csv(
            "emergency_level.csv"
        )

        print("=" * 70)
        print("RECOMMENDATION SERVICE READY")
        print("=" * 70)

    # ======================================================
    # LOAD CSV
    # ======================================================

    def load_csv(self, filename):

        file_path = self.dataset / filename

        try:

            dataframe = pd.read_csv(
                file_path,
                encoding="utf-8-sig"
            )

            # --------------------------------------------------
            # Clean column names
            # --------------------------------------------------

            dataframe.columns = [
                str(column).strip()
                for column in dataframe.columns
            ]

            # --------------------------------------------------
            # Remove completely empty rows
            # --------------------------------------------------

            dataframe = dataframe.dropna(
                how="all"
            )

            # --------------------------------------------------
            # Clean Disease column
            # --------------------------------------------------

            if "Disease" in dataframe.columns:

                dataframe["Disease"] = (
                    dataframe["Disease"]
                    .fillna("")
                    .astype(str)
                    .str.strip()
                )

            # --------------------------------------------------
            # Clean Symptom column
            # --------------------------------------------------

            if "Symptom" in dataframe.columns:

                dataframe["Symptom"] = (
                    dataframe["Symptom"]
                    .fillna("")
                    .astype(str)
                    .str.strip()
                )

            print(f"[LOADED] {filename}")

            print(
                "         Rows:",
                len(dataframe)
            )

            print(
                "         Columns:",
                list(dataframe.columns)
            )

            return dataframe

        except FileNotFoundError:

            print(
                f"[FILE NOT FOUND] {filename}"
            )

            return pd.DataFrame()

        except Exception as e:

            print(
                f"[CSV ERROR] {filename}: {e}"
            )

            return pd.DataFrame()

    # ======================================================
    # NORMALIZE DISEASE NAME
    # ======================================================

    @staticmethod
    def normalize_disease_name(disease):

        if disease is None:
            return ""

        disease = str(disease).strip().lower()

        # Brackets
        disease = disease.replace("(", " ")
        disease = disease.replace(")", " ")
        disease = disease.replace("[", " ")
        disease = disease.replace("]", " ")

        # Symbols
        disease = disease.replace("&", " and ")
        disease = disease.replace("/", " ")
        disease = disease.replace("-", " ")
        disease = disease.replace("_", " ")

        # Apostrophes
        disease = disease.replace("'", "")
        disease = disease.replace("’", "")

        # Remove unwanted characters
        disease = re.sub(
            r"[^a-z0-9\s]",
            " ",
            disease
        )

        # Remove extra spaces
        disease = re.sub(
            r"\s+",
            " ",
            disease
        )

        return disease.strip()

    # ======================================================
    # NORMALIZE SYMPTOM NAME
    # ======================================================

    @staticmethod
    def normalize_symptom_name(symptom):

        if symptom is None:
            return ""

        symptom = str(symptom).strip().lower()

        symptom = symptom.replace("_", " ")
        symptom = symptom.replace("-", " ")

        symptom = re.sub(
            r"[^a-z0-9\s]",
            " ",
            symptom
        )

        symptom = re.sub(
            r"\s+",
            " ",
            symptom
        )

        return symptom.strip()

    # ======================================================
    # FIND DISEASE ROW
    # ======================================================

    def find_row(self, dataframe, disease):

        if dataframe is None:
            return None

        if dataframe.empty:
            return None

        if "Disease" not in dataframe.columns:

            print(
                "[ERROR] Disease column not found."
            )

            print(
                "Available columns:",
                list(dataframe.columns)
            )

            return None

        target = self.normalize_disease_name(
            disease
        )

        if not target:
            return None

        # ==================================================
        # EXACT NORMALIZED MATCH
        # ==================================================

        normalized = (
            dataframe["Disease"]
            .fillna("")
            .astype(str)
            .apply(
                self.normalize_disease_name
            )
        )

        matches = dataframe[
            normalized == target
        ]

        if not matches.empty:

            original = matches.iloc[0]["Disease"]

            print(
                f"[EXACT MATCH] "
                f"{disease} -> {original}"
            )

            return matches.iloc[0]

        # ==================================================
        # PARTIAL MATCH
        # ==================================================

        for index, csv_disease in enumerate(
            normalized
        ):

            if not csv_disease:
                continue

            if (
                target in csv_disease
                or csv_disease in target
            ):

                original_name = (
                    dataframe.iloc[index]["Disease"]
                )

                print(
                    f"[PARTIAL MATCH] "
                    f"{disease} -> {original_name}"
                )

                return dataframe.iloc[index]

        # ==================================================
        # WORD-BASED MATCH
        # ==================================================

        target_words = set(
            target.split()
        )

        best_index = None
        best_score = 0

        for index, csv_disease in enumerate(
            normalized
        ):

            if not csv_disease:
                continue

            csv_words = set(
                csv_disease.split()
            )

            if not csv_words:
                continue

            common_words = (
                target_words
                .intersection(csv_words)
            )

            if not common_words:
                continue

            score = (
                len(common_words)
                /
                max(
                    len(target_words),
                    len(csv_words)
                )
            )

            if score > best_score:

                best_score = score
                best_index = index

        if (
            best_index is not None
            and best_score >= 0.5
        ):

            original_name = (
                dataframe.iloc[
                    best_index
                ]["Disease"]
            )

            print(
                f"[WORD MATCH] "
                f"{disease} -> {original_name}"
            )

            return dataframe.iloc[
                best_index
            ]

        print(
            f"[NO MATCH] '{disease}'"
        )

        return None

    # ======================================================
    # GENERIC LOOKUP
    # ======================================================

    def lookup(
        self,
        dataframe,
        disease,
        column,
        default="Not Available"
    ):

        row = self.find_row(
            dataframe,
            disease
        )

        if row is None:
            return default

        if column not in dataframe.columns:

            print(
                f"[COLUMN NOT FOUND] {column}"
            )

            print(
                "Available columns:",
                list(dataframe.columns)
            )

            return default

        value = row[column]

        if pd.isna(value):
            return default

        value = str(value).strip()

        if not value:
            return default

        # --------------------------------------------------
        # Support semicolon-separated values
        # --------------------------------------------------

        if ";" in value:

            return [
                item.strip()
                for item in value.split(";")
                if item.strip()
            ]

        return value

    # ======================================================
    # DISEASE DESCRIPTION
    #
    # SOURCE:
    # disease_causes.csv
    #
    # COLUMNS:
    # Disease
    # Description
    # ======================================================

    def get_description(self, disease):

        row = self.find_row(
            self.disease_description,
            disease
        )

        if row is None:

            print(
                "[DESCRIPTION NOT FOUND]",
                disease
            )

            return "Description not available."

        if "Description" not in (
            self.disease_description.columns
        ):

            print(
                "[DESCRIPTION ERROR] "
                "Description column not found."
            )

            return "Description not available."

        value = row["Description"]

        if pd.isna(value):
            return "Description not available."

        value = str(value).strip()

        if not value:
            return "Description not available."

        print(
            f"[DESCRIPTION FOUND] "
            f"{disease} -> {value}"
        )

        return value

    # ======================================================
    # SYMPTOM DESCRIPTION
    #
    # SOURCE:
    # symptom_description.csv
    #
    # COLUMNS:
    # Symptom
    # Description
    # ======================================================

    def get_symptom_description(
        self,
        symptom
    ):

        if self.symptom_description.empty:
            return "Symptom description not available."

        if "Symptom" not in (
            self.symptom_description.columns
        ):

            return "Symptom description not available."

        target = self.normalize_symptom_name(
            symptom
        )

        if not target:
            return "Symptom description not available."

        normalized = (
            self.symptom_description["Symptom"]
            .fillna("")
            .astype(str)
            .apply(
                self.normalize_symptom_name
            )
        )

        matches = self.symptom_description[
            normalized == target
        ]

        if matches.empty:
            return "Symptom description not available."

        row = matches.iloc[0]

        if "Description" not in (
            self.symptom_description.columns
        ):

            return "Symptom description not available."

        value = row["Description"]

        if pd.isna(value):
            return "Symptom description not available."

        value = str(value).strip()

        if not value:
            return "Symptom description not available."

        return value

    # ======================================================
    # PRECAUTIONS
    # ======================================================

    def get_precautions(self, disease):

        row = self.find_row(
            self.precaution,
            disease
        )

        if row is None:
            return []

        precautions = []

        for number in range(1, 5):

            column = f"Precaution{number}"

            if column not in self.precaution.columns:
                continue

            value = row[column]

            if pd.notna(value):

                value = str(value).strip()

                if value:
                    precautions.append(value)

        return precautions

    # ======================================================
    # DIET
    # ======================================================

    def get_diet(self, disease):

        row = self.find_row(
            self.diet,
            disease
        )

        if row is None:

            return {
                "recommended": "Not Available",
                "avoid": "Not Available"
            }

        recommended = (
            row["Recommended"]
            if "Recommended" in self.diet.columns
            else "Not Available"
        )

        avoid = (
            row["Avoid"]
            if "Avoid" in self.diet.columns
            else "Not Available"
        )

        if pd.isna(recommended):
            recommended = "Not Available"

        if pd.isna(avoid):
            avoid = "Not Available"

        return {
            "recommended": str(
                recommended
            ).strip(),

            "avoid": str(
                avoid
            ).strip()
        }

    # ======================================================
    # EXERCISE
    # ======================================================

    def get_exercise(self, disease):

        row = self.find_row(
            self.exercise,
            disease
        )

        if row is None:

            return {
                "exercise": "Not Available",
                "duration": "Not Available"
            }

        exercise = (
            row["Exercise"]
            if "Exercise" in self.exercise.columns
            else "Not Available"
        )

        duration = (
            row["Duration"]
            if "Duration" in self.exercise.columns
            else "Not Available"
        )

        if pd.isna(exercise):
            exercise = "Not Available"

        if pd.isna(duration):
            duration = "Not Available"

        return {
            "exercise": str(
                exercise
            ).strip(),

            "duration": str(
                duration
            ).strip()
        }

    # ======================================================
    # MEDICINE
    # ======================================================

    def get_medicine(self, disease):

        row = self.find_row(
            self.medicine,
            disease
        )

        if row is None:

            return {
                "medicine": "Consult Doctor",
                "type": "-"
            }

        medicine = (
            row["Medicine"]
            if "Medicine" in self.medicine.columns
            else "Consult Doctor"
        )

        medicine_type = (
            row["Type"]
            if "Type" in self.medicine.columns
            else "-"
        )

        if pd.isna(medicine):
            medicine = "Consult Doctor"

        if pd.isna(medicine_type):
            medicine_type = "-"

        return {
            "medicine": str(
                medicine
            ).strip(),

            "type": str(
                medicine_type
            ).strip()
        }

    # ======================================================
    # SPECIALIST
    # ======================================================

    def get_specialist(self, disease):

        return self.lookup(
            self.specialist,
            disease,
            "Specialist",
            "General Physician"
        )

    # ======================================================
    # HEALTH TIP
    # ======================================================

    def get_health_tip(self, disease):

        return self.lookup(
            self.health_tip,
            disease,
            "HealthTip",
            "Stay Healthy."
        )

    # ======================================================
    # CAUSES
    #
    # IMPORTANT:
    # disease_causes.csv uses the column "Description"
    #
    # Therefore causes are retrieved from Description.
    # ======================================================

    def get_causes(self, disease):

        return self.lookup(
            self.disease_description,
            disease,
            "Description",
            "Cause information not available."
        )

    # ======================================================
    # DIAGNOSIS
    # ======================================================

    def get_diagnosis(self, disease):

        return self.lookup(
            self.diagnosis,
            disease,
            "Diagnosis",
            "Diagnosis information not available."
        )

    # ======================================================
    # LAB TESTS
    # ======================================================

    def get_lab_tests(self, disease):

        return self.lookup(
            self.lab_tests,
            disease,
            "LabTests",
            "Laboratory information not available."
        )

    # ======================================================
    # RISK FACTORS
    # ======================================================

    def get_risk_factors(self, disease):

        return self.lookup(
            self.risk_factors,
            disease,
            "RiskFactors",
            "Risk-factor information not available."
        )

    # ======================================================
    # COMPLICATIONS
    # ======================================================

    def get_complications(self, disease):

        return self.lookup(
            self.complications,
            disease,
            "Complications",
            "Complication information not available."
        )

    # ======================================================
    # PREVENTION
    # ======================================================

    def get_prevention(self, disease):

        row = self.find_row(
            self.prevention,
            disease
        )

        if row is None:
            return []

        prevention = []

        for number in range(1, 4):

            column = f"Prevention{number}"

            if column not in self.prevention.columns:
                continue

            value = row[column]

            if pd.notna(value):

                value = str(value).strip()

                if value:
                    prevention.append(value)

        return prevention

    # ======================================================
    # TREATMENT
    # ======================================================

    def get_treatment(self, disease):

        return self.lookup(
            self.treatment,
            disease,
            "Treatment",
            "Treatment information not available."
        )

    # ======================================================
    # SEVERITY
    # ======================================================

    def get_severity(self, disease):

        row = self.find_row(
            self.severity,
            disease
        )

        if row is None:

            return {
                "severity": "Unknown",
                "emergency": "Unknown"
            }

        severity = "Unknown"

        if "Severity" in self.severity.columns:

            value = row["Severity"]

            if pd.notna(value):

                value = str(value).strip()

                if value:
                    severity = value

        return {
            "severity": severity,
            "emergency": "Unknown"
        }

    # ======================================================
    # EMERGENCY LEVEL
    # ======================================================

    def get_emergency(self, disease):

        row = self.find_row(
            self.emergency,
            disease
        )

        if row is None:

            return {
                "level": "Unknown",
                "action":
                    "Consult a healthcare professional."
            }

        level = "Unknown"

        action = (
            "Consult a healthcare professional."
        )

        # --------------------------------------------------
        # Emergency Level
        # --------------------------------------------------

        if "EmergencyLevel" in self.emergency.columns:

            value = row["EmergencyLevel"]

            if pd.notna(value):

                value = str(value).strip()

                if value:
                    level = value

        # --------------------------------------------------
        # Recommended Action
        # --------------------------------------------------

        if "RecommendedAction" in self.emergency.columns:

            value = row["RecommendedAction"]

            if pd.notna(value):

                value = str(value).strip()

                if value:
                    action = value

        return {
            "level": level,
            "action": action
        }

    # ======================================================
    # COMPLETE RECOMMENDATION
    # ======================================================

    def get_complete_recommendation(
        self,
        disease
    ):

        print("\n")
        print("=" * 70)
        print("DISEASE RECOMMENDATION LOOKUP")
        print("=" * 70)

        print(
            "Predicted Disease:",
            disease
        )

        print(
            "Normalized Disease:",
            self.normalize_disease_name(
                disease
            )
        )

        print("=" * 70)

        recommendation = {

            # --------------------------------------------------
            # Disease information
            # --------------------------------------------------

            "description":
                self.get_description(
                    disease
                ),

            "causes":
                self.get_causes(
                    disease
                ),

            "diagnosis":
                self.get_diagnosis(
                    disease
                ),

            "lab_tests":
                self.get_lab_tests(
                    disease
                ),

            "risk_factors":
                self.get_risk_factors(
                    disease
                ),

            "complications":
                self.get_complications(
                    disease
                ),

            "prevention":
                self.get_prevention(
                    disease
                ),

            "treatment":
                self.get_treatment(
                    disease
                ),

            # --------------------------------------------------
            # Severity
            # --------------------------------------------------

            "severity":
                self.get_severity(
                    disease
                ),

            # --------------------------------------------------
            # Emergency
            # --------------------------------------------------

            "emergency":
                self.get_emergency(
                    disease
                ),

            # --------------------------------------------------
            # Precautions
            # --------------------------------------------------

            "precautions":
                self.get_precautions(
                    disease
                ),

            # --------------------------------------------------
            # Diet
            # --------------------------------------------------

            "diet":
                self.get_diet(
                    disease
                ),

            # --------------------------------------------------
            # Exercise
            # --------------------------------------------------

            "exercise":
                self.get_exercise(
                    disease
                ),

            # --------------------------------------------------
            # Medicine
            # --------------------------------------------------

            "medicine":
                self.get_medicine(
                    disease
                ),

            # --------------------------------------------------
            # Specialist
            # --------------------------------------------------

            "specialist":
                self.get_specialist(
                    disease
                ),

            # --------------------------------------------------
            # Health Tip
            # --------------------------------------------------

            "health_tip":
                self.get_health_tip(
                    disease
                )
        }

        # ==================================================
        # DEBUG RESULT
        # ==================================================

        print("\nRECOMMENDATION RESULT")
        print("-" * 70)

        for key, value in recommendation.items():

            print(
                f"{key}: {value}"
            )

        print("=" * 70)

        return recommendation
# ==========================================================
# HEALTHCARE AI CHATBOT SERVICE
# ==========================================================

from pathlib import Path
import pandas as pd
import re
import importlib
import csv
import html


class ChatbotService:

    # ======================================================
    # INITIALIZATION
    # ======================================================

    def __init__(self):

        print()
        print("=" * 70)
        print("INITIALIZING HEALTHCARE AI CHATBOT")
        print("=" * 70)

        # --------------------------------------------------
        # Project directory
        # --------------------------------------------------

        base_dir = (
            Path(__file__)
            .resolve()
            .parent
            .parent
        )

        self.dataset_dir = base_dir / "dataset"

        print(
            "Dataset folder:",
            self.dataset_dir
        )

        # ==================================================
        # DISEASE DATASETS
        # ==================================================

        self.diet = self.load_csv(
            "diet.csv"
        )

        self.causes = self.load_csv(
            "disease_causes.csv"
        )

        self.complications = self.load_csv(
            "disease_complications.csv"
        )

        self.diagnosis = self.load_csv(
            "disease_diagnosis.csv"
        )

        self.lab_tests = self.load_csv(
            "disease_lab_tests.csv"
        )

        self.prevention = self.load_csv(
            "disease_prevention.csv"
        )

        self.risk_factors = self.load_csv(
            "disease_risk_factors.csv"
        )

        self.severity = self.load_csv(
            "disease_severity.csv"
        )

        self.treatment = self.load_csv(
            "disease_treatment.csv"
        )

        self.specialist = self.load_csv(
            "doctor_specialist.csv"
        )

        self.exercise = self.load_csv(
            "exercise.csv"
        )

        self.health_tips = self.load_csv(
            "health_tips.csv"
        )

        self.medicine = self.load_csv(
            "medicine.csv"
        )

        # ==================================================
        # SYMPTOM DATASETS
        # ==================================================

        self.symptoms_master = self.load_csv(
            "symptoms_master.csv"
        )

        self.symptom_description = self.load_csv(
            "symptom_description.csv"
        )

        self.symptom_precaution = self.load_csv(
            "symptom_precaution.csv"
        )

        # ==================================================
        # EMERGENCY DATASET
        # ==================================================

        self.emergency = (
            self.load_emergency_csv()
        )

        # ==================================================
        # DISEASE MAPPING
        # ==================================================

        self.disease_mapping = (
            self.load_disease_mapping()
        )

        # ==================================================
        # DISEASE LIST
        # ==================================================

        self.diseases = (
            self.get_disease_names()
        )

        # ==================================================
        # SYMPTOM LIST
        # ==================================================

        self.symptoms = (
            self.get_symptom_names()
        )

        print()
        print(
            "TOTAL DISEASES:",
            len(self.diseases)
        )

        print(
            "TOTAL SYMPTOMS:",
            len(self.symptoms)
        )

        print("=" * 70)
        print("CHATBOT READY")
        print("=" * 70)
        print()

    # ======================================================
    # LOAD NORMAL CSV
    # ======================================================

    def load_csv(self, filename):

        path = (
            self.dataset_dir
            / filename
        )

        try:

            if not path.exists():

                print(
                    "[WARNING] Dataset not found:",
                    filename
                )

                return pd.DataFrame()

            dataframe = pd.read_csv(
                path,
                encoding="utf-8-sig"
            )

            # Remove spaces from headers
            dataframe.columns = [
                str(column).strip()
                for column in dataframe.columns
            ]

            print(
                "[LOADED]",
                filename
            )

            print(
                "         Shape:",
                dataframe.shape
            )

            print(
                "         Columns:",
                list(dataframe.columns)
            )

            return dataframe

        except Exception as e:

            print(
                "[CSV ERROR]",
                filename,
                ":",
                e
            )

            return pd.DataFrame()

    # ======================================================
    # LOAD EMERGENCY CSV
    # ======================================================

    def load_emergency_csv(self):

        path = (
            self.dataset_dir
            / "emergency_level.csv"
        )

        columns = [
            "Disease",
            "EmergencyLevel",
            "RecommendedAction"
        ]

        if not path.exists():

            print(
                "[WARNING] Dataset not found:",
                "emergency_level.csv"
            )

            return pd.DataFrame(
                columns=columns
            )

        try:

            rows = []

            with open(
                path,
                "r",
                encoding="utf-8-sig",
                newline=""
            ) as file:

                reader = csv.reader(file)

                # Skip header
                next(
                    reader,
                    None
                )

                for parts in reader:

                    if not parts:
                        continue

                    parts = [
                        str(value).strip()
                        for value in parts
                    ]

                    if len(parts) >= 3:

                        disease = parts[0]

                        emergency_level = (
                            parts[1]
                        )

                        recommended_action = (
                            ",".join(
                                parts[2:]
                            ).strip()
                        )

                        rows.append({

                            "Disease":
                                disease,

                            "EmergencyLevel":
                                emergency_level,

                            "RecommendedAction":
                                recommended_action

                        })

            dataframe = pd.DataFrame(
                rows,
                columns=columns
            )

            print(
                "[LOADED]",
                "emergency_level.csv"
            )

            print(
                "         Shape:",
                dataframe.shape
            )

            print(
                "         Columns:",
                list(dataframe.columns)
            )

            return dataframe

        except Exception as e:

            print(
                "[ERROR] Could not load "
                "emergency_level.csv"
            )

            print(e)

            return pd.DataFrame(
                columns=columns
            )
            # ======================================================
    # LOAD DISEASE MAPPING
    # ======================================================

    def load_disease_mapping(self):

        try:

            module = importlib.import_module(
                "services.disease_mapping"
            )

            possible_names = [

                "DISEASE_MAPPING",

                "disease_mapping",

                "DISEASE_SYMPTOMS",

                "disease_symptoms",

                "MAPPING",

                "mapping"

            ]

            for name in possible_names:

                if hasattr(
                    module,
                    name
                ):

                    mapping = getattr(
                        module,
                        name
                    )

                    if isinstance(
                        mapping,
                        dict
                    ):

                        print(
                            "[LOADED] "
                            "services.disease_mapping"
                        )

                        print(
                            "         Mapped Diseases:",
                            len(mapping)
                        )

                        return mapping

            print(
                "[WARNING] Disease mapping "
                "dictionary not found."
            )

            return {}

        except Exception as e:

            print(
                "[WARNING] Could not load "
                "disease_mapping"
            )

            print(e)

            return {}

    # ======================================================
    # GET DISEASE NAMES
    # ======================================================

    def get_disease_names(self):

        names = set()

        datasets = [

            self.diet,

            self.causes,

            self.complications,

            self.diagnosis,

            self.lab_tests,

            self.prevention,

            self.risk_factors,

            self.severity,

            self.treatment,

            self.specialist,

            self.exercise,

            self.health_tips,

            self.medicine,

            self.symptom_precaution,

            self.emergency

        ]

        for dataframe in datasets:

            if dataframe.empty:
                continue

            if "Disease" not in (
                dataframe.columns
            ):
                continue

            for disease in (
                dataframe["Disease"]
                .dropna()
            ):

                disease = str(
                    disease
                ).strip()

                if disease:

                    names.add(
                        disease
                    )

        # Add mapping diseases
        for disease in (
            self.disease_mapping.keys()
        ):

            disease = str(
                disease
            ).strip()

            if disease:

                names.add(
                    disease
                )

        return sorted(
            names,
            key=len,
            reverse=True
        )

    # ======================================================
    # GET SYMPTOM NAMES
    # ======================================================

    def get_symptom_names(self):

        symptoms = set()

        # --------------------------------------------------
        # symptoms_master.csv
        # --------------------------------------------------

        if not self.symptoms_master.empty:

            possible_columns = [

                "Symptom",
                "Symptoms",
                "symptom",
                "symptoms"

            ]

            for column in possible_columns:

                if column in (
                    self.symptoms_master.columns
                ):

                    for value in (
                        self.symptoms_master[
                            column
                        ].dropna()
                    ):

                        value = str(
                            value
                        ).strip()

                        if value:

                            symptoms.add(
                                value
                            )

        # --------------------------------------------------
        # symptom_description.csv
        # --------------------------------------------------

        if not self.symptom_description.empty:

            if "Symptom" in (
                self.symptom_description.columns
            ):

                for value in (
                    self.symptom_description[
                        "Symptom"
                    ].dropna()
                ):

                    value = str(
                        value
                    ).strip()

                    if value:

                        symptoms.add(
                            value
                        )

        # --------------------------------------------------
        # Python symptom master
        # --------------------------------------------------

        try:

            module = importlib.import_module(
                "services.symptoms_master"
            )

            if hasattr(
                module,
                "SYMPTOMS"
            ):

                master = module.SYMPTOMS

                if isinstance(
                    master,
                    (list, tuple, set)
                ):

                    for value in master:

                        value = str(
                            value
                        ).strip()

                        if value:

                            symptoms.add(
                                value
                            )

        except Exception:

            pass

        return sorted(
            symptoms,
            key=len,
            reverse=True
        )

    # ======================================================
    # NORMALIZE TEXT
    # ======================================================

    def normalize(self, text):

        text = str(
            text
        ).lower().strip()

        text = text.replace(
            "_",
            " "
        )

        text = re.sub(
            r"[^a-z0-9\s]",
            " ",
            text
        )

        text = re.sub(
            r"\s+",
            " ",
            text
        )

        return text.strip()

    # ======================================================
    # SAFE HTML TEXT
    # ======================================================

    def safe_text(self, value):

        if value is None:

            return ""

        try:

            if pd.isna(value):

                return ""

        except Exception:

            pass

        return html.escape(
            str(value).strip()
        )

    # ======================================================
    # FIND DISEASE
    # ======================================================

    def find_disease(self, message):

        normalized_message = (
            self.normalize(
                message
            )
        )

        if not normalized_message:

            return None

        # --------------------------------------------------
        # Exact / longest match
        # --------------------------------------------------

        for disease in self.diseases:

            normalized_disease = (
                self.normalize(
                    disease
                )
            )

            if not normalized_disease:

                continue

            if normalized_disease in (
                normalized_message
            ):

                return disease

        # --------------------------------------------------
        # Word matching
        # --------------------------------------------------

        message_words = set(
            normalized_message.split()
        )

        best_disease = None

        best_score = 0

        for disease in self.diseases:

            disease_words = set(
                self.normalize(
                    disease
                ).split()
            )

            if not disease_words:

                continue

            matched_words = (
                disease_words
                .intersection(
                    message_words
                )
            )

            score = len(
                matched_words
            )

            if score > best_score:

                best_score = score

                best_disease = disease

        if best_score > 0:

            return best_disease

        return None

    # ======================================================
    # FIND SYMPTOM
    # ======================================================

    def find_symptom(self, message):

        normalized_message = (
            self.normalize(
                message
            )
        )

        for symptom in self.symptoms:

            normalized_symptom = (
                self.normalize(
                    symptom
                )
            )

            if not normalized_symptom:

                continue

            if normalized_symptom in (
                normalized_message
            ):

                return symptom

        return None

    # ======================================================
    # GET DISEASE ROW
    # ======================================================

    def get_disease_row(
        self,
        dataframe,
        disease
    ):

        if dataframe is None:

            return None

        if dataframe.empty:

            return None

        if "Disease" not in (
            dataframe.columns
        ):

            return None

        wanted = self.normalize(
            disease
        )

        # Exact normalized match
        for _, row in (
            dataframe.iterrows()
        ):

            current = self.normalize(
                row.get(
                    "Disease",
                    ""
                )
            )

            if current == wanted:

                return row

        # Partial match
        for _, row in (
            dataframe.iterrows()
        ):

            current = self.normalize(
                row.get(
                    "Disease",
                    ""
                )
            )

            if (
                current in wanted
                or wanted in current
            ):

                return row

        return None

    # ======================================================
    # GENERIC DATASET LOOKUP
    # ======================================================

    def lookup(
        self,
        dataframe,
        disease,
        column,
        default="Information not available."
    ):

        row = self.get_disease_row(
            dataframe,
            disease
        )

        if row is None:

            return default

        if column not in (
            dataframe.columns
        ):

            return default

        value = row.get(
            column,
            ""
        )

        if pd.isna(value):

            return default

        value = str(
            value
        ).strip()

        if not value:

            return default

        return self.safe_text(
            value
        )

    # ======================================================
    # FORMAT LIST
    # ======================================================

    def format_list(self, value):

        if value is None:

            return (
                "<p>"
                "Information not available."
                "</p>"
            )

        if isinstance(
            value,
            (list, tuple, set)
        ):

            items = value

        else:

            value = str(
                value
            ).strip()

            if not value:

                return (
                    "<p>"
                    "Information not available."
                    "</p>"
                )

            if ";" in value:

                items = value.split(";")

            elif "|" in value:

                items = value.split("|")

            else:

                items = [
                    value
                ]

        cleaned = []

        for item in items:

            item = str(
                item
            ).strip()

            if item:

                cleaned.append(
                    self.safe_text(
                        item
                    )
                )

        if not cleaned:

            return (
                "<p>"
                "Information not available."
                "</p>"
            )

        result = "<ul>"

        for item in cleaned:

            result += (
                "<li>"
                + item
                + "</li>"
            )

        result += "</ul>"

        return result
        # ======================================================
    # DISEASE SYMPTOMS
    # ======================================================

    def get_disease_symptoms(
        self,
        disease
    ):

        if not self.disease_mapping:

            return (
                "<p>"
                "Disease symptom mapping "
                "is not available."
                "</p>"
            )

        wanted = self.normalize(
            disease
        )

        matched_value = None

        # --------------------------------------------------
        # Exact disease match
        # --------------------------------------------------

        for key, value in (
            self.disease_mapping.items()
        ):

            if (
                self.normalize(
                    key
                )
                == wanted
            ):

                matched_value = value

                break

        # --------------------------------------------------
        # Partial disease match
        # --------------------------------------------------

        if matched_value is None:

            for key, value in (
                self.disease_mapping.items()
            ):

                key_normalized = (
                    self.normalize(
                        key
                    )
                )

                if (
                    key_normalized in wanted
                    or wanted in key_normalized
                ):

                    matched_value = value

                    break

        if matched_value is None:

            return (
                "<p>"
                "Symptoms for "
                + self.safe_text(
                    disease
                )
                + " are not available."
                "</p>"
            )

        # --------------------------------------------------
        # Convert mapping into list
        # --------------------------------------------------

        if isinstance(
            matched_value,
            str
        ):

            symptom_list = re.split(
                r"[,;|]",
                matched_value
            )

        elif isinstance(
            matched_value,
            dict
        ):

            symptom_list = []

            for value in (
                matched_value.values()
            ):

                if isinstance(
                    value,
                    (list, tuple, set)
                ):

                    symptom_list.extend(
                        value
                    )

                else:

                    symptom_list.append(
                        value
                    )

        elif isinstance(
            matched_value,
            (list, tuple, set)
        ):

            symptom_list = list(
                matched_value
            )

        else:

            symptom_list = [
                matched_value
            ]

        # --------------------------------------------------
        # Create HTML
        # --------------------------------------------------

        result = "<ul>"

        count = 0

        for symptom in symptom_list:

            symptom_text = str(
                symptom
            ).strip()

            if not symptom_text:

                continue

            readable = (
                symptom_text
                .replace(
                    "_",
                    " "
                )
                .strip()
                .title()
            )

            result += (
                "<li>"
                + self.safe_text(
                    readable
                )
                + "</li>"
            )

            count += 1

        result += "</ul>"

        if count == 0:

            return (
                "<p>"
                "Symptoms for this disease "
                "are not available."
                "</p>"
            )

        return result

    # ======================================================
    # INDIVIDUAL SYMPTOM DESCRIPTION
    # ======================================================

    def get_symptom_description(
        self,
        symptom
    ):

        wanted = self.normalize(
            symptom
        )

        # --------------------------------------------------
        # FIRST: symptoms_master.csv
        # --------------------------------------------------

        if not self.symptoms_master.empty:

            if "Symptom" in (
                self.symptoms_master.columns
            ):

                for _, row in (
                    self.symptoms_master.iterrows()
                ):

                    current = self.normalize(
                        row.get(
                            "Symptom",
                            ""
                        )
                    )

                    if current == wanted:

                        possible_columns = [

                            "Description",
                            "description",
                            "Meaning",
                            "meaning"

                        ]

                        for column in (
                            possible_columns
                        ):

                            if column in (
                                self.symptoms_master.columns
                            ):

                                value = row.get(
                                    column,
                                    ""
                                )

                                if pd.notna(
                                    value
                                ):

                                    value = str(
                                        value
                                    ).strip()

                                    if value:

                                        return self.safe_text(
                                            value
                                        )

        # --------------------------------------------------
        # SECOND: symptom_description.csv
        # --------------------------------------------------

        if not self.symptom_description.empty:

            if (
                "Symptom"
                in self.symptom_description.columns
                and
                "Description"
                in self.symptom_description.columns
            ):

                for _, row in (
                    self.symptom_description.iterrows()
                ):

                    current = self.normalize(
                        row.get(
                            "Symptom",
                            ""
                        )
                    )

                    if current == wanted:

                        value = row.get(
                            "Description",
                            ""
                        )

                        if pd.notna(
                            value
                        ):

                            value = str(
                                value
                            ).strip()

                            if value:

                                return self.safe_text(
                                    value
                                )

        return (
            "Symptom information "
            "not available."
        )

    # ======================================================
    # DESCRIPTION
    # ======================================================

    def get_description(
        self,
        disease
    ):

        return self.lookup(
            self.causes,
            disease,
            "Description",
            "Disease description not available."
        )

    # ======================================================
    # CAUSES
    # ======================================================

    def get_causes(
        self,
        disease
    ):

        return self.lookup(
            self.causes,
            disease,
            "Description",
            "Cause information not available."
        )

    # ======================================================
    # DIAGNOSIS
    # ======================================================

    def get_diagnosis(
        self,
        disease
    ):

        return self.lookup(
            self.diagnosis,
            disease,
            "Diagnosis",
            "Diagnosis information not available."
        )

    # ======================================================
    # LAB TESTS
    # ======================================================

    def get_lab_tests(
        self,
        disease
    ):

        value = self.lookup(
            self.lab_tests,
            disease,
            "LabTests",
            "Laboratory test information not available."
        )

        return self.format_list(
            value
        )

    # ======================================================
    # RISK FACTORS
    # ======================================================

    def get_risk_factors(
        self,
        disease
    ):

        value = self.lookup(
            self.risk_factors,
            disease,
            "RiskFactors",
            "Risk factor information not available."
        )

        return self.format_list(
            value
        )

    # ======================================================
    # COMPLICATIONS
    # ======================================================

    def get_complications(
        self,
        disease
    ):

        value = self.lookup(
            self.complications,
            disease,
            "Complications",
            "Complication information not available."
        )

        return self.format_list(
            value
        )

    # ======================================================
    # PREVENTION
    # ======================================================

    def get_prevention(
        self,
        disease
    ):

        row = self.get_disease_row(
            self.prevention,
            disease
        )

        if row is None:

            return (
                "<p>"
                "Prevention information "
                "not available."
                "</p>"
            )

        result = "<ul>"

        count = 0

        for number in range(1, 4):

            column = (
                "Prevention"
                + str(number)
            )

            if column not in (
                self.prevention.columns
            ):

                continue

            value = row.get(
                column,
                ""
            )

            if pd.notna(
                value
            ):

                value = str(
                    value
                ).strip()

                if value:

                    result += (
                        "<li>"
                        + self.safe_text(
                            value
                        )
                        + "</li>"
                    )

                    count += 1

        result += "</ul>"

        if count == 0:

            return (
                "<p>"
                "Prevention information "
                "not available."
                "</p>"
            )

        return result

    # ======================================================
    # TREATMENT
    # ======================================================

    def get_treatment(
        self,
        disease
    ):

        return self.lookup(
            self.treatment,
            disease,
            "Treatment",
            "Treatment information not available."
        )

    # ======================================================
    # SEVERITY
    # ======================================================

    def get_severity(
        self,
        disease
    ):

        return self.lookup(
            self.severity,
            disease,
            "Severity",
            "Severity information not available."
        )

    # ======================================================
    # SPECIALIST
    # ======================================================

    def get_specialist(
        self,
        disease
    ):

        return self.lookup(
            self.specialist,
            disease,
            "Specialist",
            "Specialist information not available."
        )

    # ======================================================
    # HEALTH TIP
    # ======================================================

    def get_health_tip(
        self,
        disease
    ):

        return self.lookup(
            self.health_tips,
            disease,
            "HealthTip",
            "Health tip information not available."
        )
        # ======================================================
    # DIET
    # ======================================================

    def get_diet(
        self,
        disease
    ):

        recommended = self.lookup(
            self.diet,
            disease,
            "Recommended",
            "Recommended food information not available."
        )

        avoid = self.lookup(
            self.diet,
            disease,
            "Avoid",
            "Food to avoid information not available."
        )

        result = (

            "<div class='chat-section'>"

            "<h6>🥗 Recommended Foods</h6>"

            + self.format_list(
                recommended
            )

            + "<h6>🚫 Foods to Avoid</h6>"

            + self.format_list(
                avoid
            )

            + "</div>"

        )

        return result

    # ======================================================
    # EXERCISE
    # ======================================================

    def get_exercise(
        self,
        disease
    ):

        exercise = self.lookup(
            self.exercise,
            disease,
            "Exercise",
            "Exercise information not available."
        )

        duration = self.lookup(
            self.exercise,
            disease,
            "Duration",
            "Duration information not available."
        )

        result = (

            "<h6>🏃 Exercise</h6>"

            + self.format_list(
                exercise
            )

            + "<h6>⏱ Duration</h6>"

            + "<p>"
            + duration
            + "</p>"

        )

        return result

    # ======================================================
    # MEDICINE
    # ======================================================

    def get_medicine(
        self,
        disease
    ):

        medicine = self.lookup(
            self.medicine,
            disease,
            "Medicine",
            "Medicine information not available."
        )

        medicine_type = self.lookup(
            self.medicine,
            disease,
            "Type",
            "Medicine type information not available."
        )

        result = (

            "<h6>💊 Medicine</h6>"

            + self.format_list(
                medicine
            )

            + "<h6>Medicine Type</h6>"

            + "<p>"
            + medicine_type
            + "</p>"

            + "<p>"
            "<strong>Disclaimer:</strong> "
            "Medicine information is provided "
            "for educational purposes only. "
            "Consult a qualified healthcare "
            "professional before taking medicine."
            "</p>"

        )

        return result

    # ======================================================
    # EMERGENCY
    # ======================================================

    def get_emergency(
        self,
        disease
    ):

        if self.emergency.empty:

            return (
                "<p>"
                "Emergency information "
                "not available."
                "</p>"
            )

        level = self.lookup(
            self.emergency,
            disease,
            "EmergencyLevel",
            "Not available."
        )

        action = self.lookup(
            self.emergency,
            disease,
            "RecommendedAction",
            "Please consult a qualified healthcare professional."
        )

        result = (

            "<h6>🚨 Emergency Level</h6>"

            "<p>"
            "<strong>"
            + level
            + "</strong>"
            "</p>"

            "<h6>Recommended Action</h6>"

            "<p>"
            + action
            + "</p>"

        )

        return result

    # ======================================================
    # PRECAUTIONS
    # ======================================================

    def get_precautions(
        self,
        disease
    ):

        row = self.get_disease_row(
            self.symptom_precaution,
            disease
        )

        if row is None:

            return (
                "<p>"
                "Precaution information "
                "not available."
                "</p>"
            )

        result = "<ul>"

        count = 0

        for number in range(1, 5):

            column = (
                "Precaution"
                + str(number)
            )

            if column not in (
                self.symptom_precaution.columns
            ):

                continue

            value = row.get(
                column,
                ""
            )

            if pd.notna(
                value
            ):

                value = str(
                    value
                ).strip()

                if value:

                    result += (
                        "<li>"
                        + self.safe_text(
                            value
                        )
                        + "</li>"
                    )

                    count += 1

        result += "</ul>"

        if count == 0:

            return (
                "<p>"
                "Precaution information "
                "not available."
                "</p>"
            )

        return result

    # ======================================================
    # DISEASE OVERVIEW
    # ======================================================

    def get_disease_overview(
        self,
        disease
    ):

        description = self.get_description(
            disease
        )

        result = (

            "<div class='chat-section'>"

            "<div class='chat-section-title'>"
            "🩺 "
            + self.safe_text(
                disease
            )
            + "</div>"

            "<div class='chat-section-text'>"
            + description
            + "</div>"

            "<div class='chat-section-help'>"
            "You can ask me about:"
            "</div>"

            "<ul>"

            "<li>Symptoms</li>"
            "<li>Causes</li>"
            "<li>Diagnosis</li>"
            "<li>Lab tests</li>"
            "<li>Risk factors</li>"
            "<li>Complications</li>"
            "<li>Prevention</li>"
            "<li>Treatment</li>"
            "<li>Severity</li>"
            "<li>Emergency level</li>"
            "<li>Diet</li>"
            "<li>Exercise</li>"
            "<li>Medicines</li>"
            "<li>Specialist</li>"
            "<li>Precautions</li>"
            "<li>Health tips</li>"

            "</ul>"

            "</div>"

        )

        return result

    # ======================================================
    # COMPLETE DISEASE INFORMATION
    # ======================================================

    def get_complete_recommendation(
        self,
        disease
    ):

        disease_name = self.safe_text(
            disease
        )

        description = (
            self.get_description(
                disease
            )
        )

        symptoms = (
            self.get_disease_symptoms(
                disease
            )
        )

        causes = (
            self.get_causes(
                disease
            )
        )

        diagnosis = (
            self.get_diagnosis(
                disease
            )
        )

        lab_tests = (
            self.get_lab_tests(
                disease
            )
        )

        risk_factors = (
            self.get_risk_factors(
                disease
            )
        )

        complications = (
            self.get_complications(
                disease
            )
        )

        prevention = (
            self.get_prevention(
                disease
            )
        )

        treatment = (
            self.get_treatment(
                disease
            )
        )

        severity = (
            self.get_severity(
                disease
            )
        )

        emergency = (
            self.get_emergency(
                disease
            )
        )

        precautions = (
            self.get_precautions(
                disease
            )
        )

        diet = (
            self.get_diet(
                disease
            )
        )

        exercise = (
            self.get_exercise(
                disease
            )
        )

        medicine = (
            self.get_medicine(
                disease
            )
        )

        specialist = (
            self.get_specialist(
                disease
            )
        )

        health_tip = (
            self.get_health_tip(
                disease
            )
        )

        result = (

            "<div class='chat-section'>"

            "<div class='chat-section-title'>"
            "🩺 "
            + disease_name
            + " - Complete Information"
            + "</div>"

            "<h6>📖 Description</h6>"

            "<p>"
            + description
            + "</p>"

            "<h6>🦠 Symptoms</h6>"

            + symptoms

            + "<h6>❓ Causes</h6>"

            "<p>"
            + causes
            + "</p>"

            "<h6>🔍 Diagnosis</h6>"

            "<p>"
            + diagnosis
            + "</p>"

            "<h6>🧪 Laboratory Tests</h6>"

            + lab_tests

            + "<h6>⚠️ Risk Factors</h6>"

            + risk_factors

            + "<h6>🩹 Complications</h6>"

            + complications

            + "<h6>🛡️ Prevention</h6>"

            + prevention

            + "<h6>💚 Treatment</h6>"

            "<p>"
            + treatment
            + "</p>"

            "<h6>📊 Severity</h6>"

            "<p>"
            + severity
            + "</p>"

            + "<h6>🚨 Emergency Information</h6>"

            + emergency

            + "<h6>📝 Precautions</h6>"

            + precautions

            + "<h6>🥗 Diet</h6>"

            + diet

            + "<h6>🏃 Exercise</h6>"

            + exercise

            + "<h6>💊 Medicine</h6>"

            + medicine

            + "<h6>👨‍⚕️ Specialist</h6>"

            "<p>"
            + specialist
            + "</p>"

            "<h6>❤️ Health Tip</h6>"

            "<p>"
            + health_tip
            + "</p>"

            "</div>"

        )

        return result
        # ======================================================
    # PROJECT RELATED QUESTIONS
    # ======================================================

    def project_response(
        self,
        text
    ):

        # ==================================================
        # WHAT IS PROJECT
        # ==================================================

        if (
            "what is the project" in text
            or "about the project" in text
            or "project about" in text
            or "explain the project" in text
        ):

            return (

                "<h6>🏥 Healthcare AI Project</h6>"

                "<p>"
                "This project is a web-based "
                "AI Healthcare application."
                "</p>"

                "<p>"
                "The system allows users to select "
                "symptoms and obtain a possible disease "
                "prediction using a trained Machine "
                "Learning model."
                "</p>"

                "<p>"
                "After prediction, the system retrieves "
                "disease-specific information from "
                "separate healthcare CSV datasets."
                "</p>"

                "<p>"
                "The project also provides an AI chatbot, "
                "prediction history, profile management, "
                "PDF reports and an Admin Panel."
                "</p>"

            )

        # ==================================================
        # AIM / OBJECTIVE
        # ==================================================

        if (
            "objective" in text
            or "objectives" in text
            or "aim of the project" in text
            or text == "aim"
            or "purpose of the project" in text
        ):

            return (

                "<h6>🎯 Aim and Objectives</h6>"

                "<p>"
                "The main aim is to develop a web-based "
                "Healthcare AI application that predicts "
                "a possible disease from symptoms and "
                "provides disease-specific healthcare "
                "information."
                "</p>"

                "<ul>"

                "<li>User registration and login</li>"

                "<li>"
                "Symptom selection"
                "</li>"

                "<li>"
                "Machine Learning disease prediction"
                "</li>"

                "<li>"
                "Prediction confidence and top predictions"
                "</li>"

                "<li>"
                "Disease-specific recommendations"
                "</li>"

                "<li>"
                "Healthcare chatbot"
                "</li>"

                "<li>"
                "Project-information chatbot"
                "</li>"

                "<li>"
                "Prediction history"
                "</li>"

                "<li>"
                "PDF report generation"
                "</li>"

                "<li>"
                "Admin management"
                "</li>"

                "</ul>"

            )

        # ==================================================
        # TECHNOLOGIES
        # ==================================================

        if (
            "technology" in text
            or "technologies" in text
            or "tech stack" in text
            or "technology used" in text
            or "technologies used" in text
        ):

            return (

                "<h6>💻 Technologies Used</h6>"

                "<ul>"

                "<li>Python</li>"
                "<li>Flask</li>"
                "<li>HTML</li>"
                "<li>CSS</li>"
                "<li>JavaScript</li>"
                "<li>Bootstrap</li>"
                "<li>Pandas</li>"
                "<li>scikit-learn</li>"
                "<li>Joblib</li>"
                "<li>CSV datasets</li>"
                "<li>Oracle Database</li>"
                "<li>ReportLab</li>"

                "</ul>"

            )

        # ==================================================
        # PROJECT WORKING
        # ==================================================

        if (
            "how does the project work" in text
            or "how project works" in text
            or "project workflow" in text
            or "working of the project" in text
        ):

            return (

                "<h6>⚙️ How the Project Works</h6>"

                "<ol>"

                "<li>"
                "User registers or logs in."
                "</li>"

                "<li>"
                "User selects symptoms."
                "</li>"

                "<li>"
                "The application validates the selected symptoms."
                "</li>"

                "<li>"
                "The symptoms are sent to the Machine Learning model."
                "</li>"

                "<li>"
                "The model predicts a possible disease."
                "</li>"

                "<li>"
                "The model returns confidence and top predictions."
                "</li>"

                "<li>"
                "Recommendation Service retrieves disease information."
                "</li>"

                "<li>"
                "The prediction is stored in prediction history."
                "</li>"

                "<li>"
                "The result is displayed to the user."
                "</li>"

                "<li>"
                "The user can download a PDF report."
                "</li>"

                "<li>"
                "The chatbot answers healthcare and project questions."
                "</li>"

                "</ol>"

            )

        # ==================================================
        # MACHINE LEARNING
        # ==================================================

        if (
            "machine learning" in text
            or "machine learning model" in text
            or "ml model" in text
            or "what is ml" in text
        ):

            return (

                "<h6>🤖 Machine Learning Module</h6>"

                "<p>"
                "Machine Learning is used to predict "
                "a possible disease from the symptoms "
                "selected by the user."
                "</p>"

                "<p>"
                "The selected symptoms are converted "
                "into the input format expected by the "
                "trained model."
                "</p>"

                "<p>"
                "The model returns a predicted disease, "
                "confidence and top prediction candidates."
                "</p>"

            )

        # ==================================================
        # RECOMMENDATION SERVICE
        # ==================================================

        if (
            "recommendation service" in text
            or "recommendation system" in text
            or "what is recommendation" in text
            or "how recommendation works" in text
        ):

            return (

                "<h6>📋 Recommendation Service</h6>"

                "<p>"
                "The Recommendation Service connects "
                "a disease with the correct healthcare "
                "dataset and retrieves the required information."
                "</p>"

                "<p>"
                "It can retrieve diet, exercise, medicine, "
                "specialist, health tips, prevention, "
                "precautions and other disease information."
                "</p>"

                "<p>"
                "The common key used for disease-specific "
                "datasets is the Disease field."
                "</p>"

            )

        # ==================================================
        # CHATBOT
        # ==================================================

        if (
            "what is chatbot" in text
            or "how chatbot works" in text
            or "how does chatbot work" in text
            or "chatbot service" in text
            or "about chatbot" in text
        ):

            return (

                "<h6>🤖 AI Healthcare Chatbot</h6>"

                "<p>"
                "The chatbot accepts questions written "
                "in normal language."
                "</p>"

                "<p>"
                "It identifies whether the question is "
                "a greeting, project question, disease "
                "question or symptom question."
                "</p>"

                "<p>"
                "For disease questions, it identifies "
                "the disease and retrieves information "
                "from the appropriate dataset."
                "</p>"

                "<p>"
                "For disease-specific symptom questions, "
                "the chatbot uses disease mapping so that "
                "only the requested disease's symptoms "
                "are returned."
                "</p>"

            )

        # ==================================================
        # DATASETS
        # ==================================================

        if (
            "dataset" in text
            or "datasets" in text
            or "csv files" in text
            or "data used" in text
            or "which datasets" in text
        ):

            return (

                "<h6>📊 Healthcare Datasets</h6>"

                "<p>"
                "The project uses separate CSV files "
                "for different healthcare information."
                "</p>"

                "<ul>"

                "<li>diet.csv</li>"
                "<li>symptoms_master.csv</li>"
                "<li>symptom_description.csv</li>"
                "<li>symptom_precaution.csv</li>"
                "<li>disease_causes.csv</li>"
                "<li>disease_complications.csv</li>"
                "<li>disease_diagnosis.csv</li>"
                "<li>disease_lab_tests.csv</li>"
                "<li>disease_prevention.csv</li>"
                "<li>disease_risk_factors.csv</li>"
                "<li>disease_severity.csv</li>"
                "<li>disease_treatment.csv</li>"
                "<li>doctor_specialist.csv</li>"
                "<li>exercise.csv</li>"
                "<li>health_tips.csv</li>"
                "<li>medicine.csv</li>"
                "<li>emergency_level.csv</li>"

                "</ul>"

            )

        # ==================================================
        # DATABASE
        # ==================================================

        if (
            "database" in text
            or "oracle database" in text
            or text == "oracle"
        ):

            return (

                "<h6>🗄️ Database</h6>"

                "<p>"
                "The project uses Oracle Database for "
                "persistent application information "
                "where configured."
                "</p>"

                "<p>"
                "User information, profile information "
                "and prediction history can be stored "
                "in the database."
                "</p>"

            )

        # ==================================================
        # ADMIN PANEL
        # ==================================================

        if (
            "admin panel" in text
            or "admin page" in text
            or "administrator" in text
            or "what is admin" in text
        ):

            return (

                "<h6>👨‍💼 Admin Panel</h6>"

                "<p>"
                "The Admin Panel is the administrative "
                "area of the Healthcare AI application."
                "</p>"

                "<p>"
                "It is intended for authorized administrators "
                "and provides management and monitoring "
                "functions supported by the application."
                "</p>"

                "<ul>"

                "<li>User management</li>"
                "<li>Prediction monitoring</li>"
                "<li>History monitoring</li>"
                "<li>Dataset management</li>"
                "<li>Application information</li>"

                "</ul>"

            )

        # ==================================================
        # HISTORY
        # ==================================================

        if (
            "prediction history" in text
            or text == "history"
            or "what is history" in text
        ):

            return (

                "<h6>🕒 Prediction History</h6>"

                "<p>"
                "Prediction History stores the user's "
                "previous disease predictions."
                "</p>"

                "<p>"
                "A history record can contain the disease, "
                "confidence, selected symptoms and prediction date."
                "</p>"

                "<p>"
                "The user can open the History page to "
                "review previous predictions."
                "</p>"

            )

        # ==================================================
        # PDF REPORT
        # ==================================================

        if (
            "pdf" in text
            or "pdf report" in text
            or "report generation" in text
        ):

            return (

                "<h6>📄 PDF Report</h6>"

                "<p>"
                "The project can generate a downloadable "
                "PDF report containing prediction information."
                "</p>"

                "<ul>"

                "<li>User information</li>"
                "<li>Selected symptoms</li>"
                "<li>Predicted disease</li>"
                "<li>Confidence</li>"
                "<li>Top predictions</li>"
                "<li>Disease information</li>"
                "<li>Recommendations</li>"

                "</ul>"

                "<p>"
                "ReportLab is used for PDF generation."
                "</p>"

            )

        # ==================================================
        # ADVANTAGES
        # ==================================================

        if (
            "advantages" in text
            or "benefits of project" in text
            or text == "benefits"
        ):

            return (

                "<h6>✅ Advantages</h6>"

                "<ul>"

                "<li>"
                "Disease prediction and healthcare information "
                "are combined in one application."
                "</li>"

                "<li>"
                "Disease-specific chatbot responses."
                "</li>"

                "<li>"
                "Separate CSV datasets are easier to maintain."
                "</li>"

                "<li>"
                "Prediction history is available."
                "</li>"

                "<li>"
                "PDF reports can be generated."
                "</li>"

                "<li>"
                "Responsive web interface."
                "</li>"

                "<li>"
                "Admin management support."
                "</li>"

                "</ul>"

            )

        # ==================================================
        # LIMITATIONS
        # ==================================================

        if (
            "limitations" in text
            or "disadvantages" in text
        ):

            return (

                "<h6>⚠️ Limitations</h6>"

                "<ul>"

                "<li>"
                "The prediction is preliminary and "
                "is not a confirmed medical diagnosis."
                "</li>"

                "<li>"
                "Performance depends on the quality "
                "of the training dataset."
                "</li>"

                "<li>"
                "CSV files must contain the correct headers."
                "</li>"

                "<li>"
                "Natural-language questions can sometimes "
                "be ambiguous."
                "</li>"

                "<li>"
                "Only diseases available in the datasets "
                "can be handled properly."
                "</li>"

                "</ul>"

            )

        # ==================================================
        # FUTURE SCOPE
        # ==================================================

        if (
            "future scope" in text
            or "future enhancement" in text
            or "future work" in text
        ):

            return (

                "<h6>🚀 Future Scope</h6>"

                "<ul>"

                "<li>"
                "Add more diseases and symptoms."
                "</li>"

                "<li>"
                "Use larger and medically validated datasets."
                "</li>"

                "<li>"
                "Add Kannada and other Indian languages."
                "</li>"

                "<li>"
                "Improve natural-language understanding."
                "</li>"

                "<li>"
                "Add spelling correction and symptom synonyms."
                "</li>"

                "<li>"
                "Add Explainable AI."
                "</li>"

                "<li>"
                "Improve Admin analytics."
                "</li>"

                "<li>"
                "Improve voice input and voice output."
                "</li>"

                "</ul>"

            )

        # ==================================================
        # PROJECT STRUCTURE
        # ==================================================

        if (
            "project structure" in text
            or "folder structure" in text
            or "files in project" in text
        ):

            return (

                "<h6>📁 Project Structure</h6>"

                "<ul>"

                "<li>app.py</li>"
                "<li>config.py</li>"
                "<li>db.py</li>"
                "<li>ml/predict.py</li>"
                "<li>routes/auth.py</li>"
                "<li>routes/prediction.py</li>"
                "<li>routes/profile.py</li>"
                "<li>routes/history.py</li>"
                "<li>routes/admin.py</li>"
                "<li>services/recommendation_service.py</li>"
                "<li>services/chatbot_service.py</li>"
                "<li>services/history_service.py</li>"
                "<li>services/pdf_service.py</li>"
                "<li>dataset/</li>"
                "<li>templates/</li>"
                "<li>static/</li>"

                "</ul>"

            )

        # ==================================================
        # CONCLUSION
        # ==================================================

        if (
            "conclusion" in text
            or "summarize project" in text
            or "summary of project" in text
        ):

            return (

                "<h6>📝 Project Conclusion</h6>"

                "<p>"
                "The Healthcare AI project combines "
                "Machine Learning, healthcare datasets "
                "and web technologies into one application."
                "</p>"

                "<p>"
                "Users can select symptoms and receive "
                "a possible disease prediction."
                "</p>"

                "<p>"
                "The Recommendation Service retrieves "
                "disease-specific healthcare information."
                "</p>"

                "<p>"
                "The chatbot provides both healthcare "
                "information and project-related information."
                "</p>"

                "<p>"
                "The application also includes authentication, "
                "profile management, prediction history, "
                "PDF reporting and an Admin Panel."
                "</p>"

            )

        return None

    # ======================================================
    # HELP
    # ======================================================

    def get_help(self):

        return (

            "<h6>🤖 Healthcare AI Assistant</h6>"

            "<p>"
            "I can answer questions about diseases, "
            "symptoms and your Healthcare AI project."
            "</p>"

            "<h6>🏥 Healthcare Questions</h6>"

            "<ul>"

            "<li>"
            "What are the symptoms of Typhoid?"
            "</li>"

            "<li>"
            "What causes Diabetes?"
            "</li>"

            "<li>"
            "What is the diet for Dengue?"
            "</li>"

            "<li>"
            "What exercise is recommended for Asthma?"
            "</li>"

            "<li>"
            "What medicines are listed for Malaria?"
            "</li>"

            "<li>"
            "What are the precautions for Typhoid?"
            "</li>"

            "<li>"
            "What tests are used for Dengue?"
            "</li>"

            "<li>"
            "Who is the specialist for Diabetes?"
            "</li>"

            "</ul>"

            "<h6>💻 Project Questions</h6>"

            "<ul>"

            "<li>What is this project?</li>"
            "<li>What is the objective?</li>"
            "<li>How does the project work?</li>"
            "<li>Which technologies are used?</li>"
            "<li>What is Machine Learning doing?</li>"
            "<li>What is Recommendation Service?</li>"
            "<li>What datasets are used?</li>"
            "<li>What is the Admin Panel?</li>"
            "<li>What database is used?</li>"
            "<li>What are the advantages?</li>"
            "<li>What are the limitations?</li>"
            "<li>What is the future scope?</li>"

            "</ul>"

        )

    # ======================================================
    # MAIN CHATBOT RESPONSE
    # ======================================================

    def get_response(
        self,
        message
    ):

        if message is None:

            return self.get_help()

        original_message = str(
            message
        ).strip()

        if not original_message:

            return (
                "Please type a question."
            )

        text = self.normalize(
            original_message
        )

        # ==================================================
        # GREETINGS
        # ==================================================

        greeting_words = [

            "hi",
            "hello",
            "hey",
            "hai",
            "good morning",
            "good afternoon",
            "good evening"

        ]

        if text in greeting_words:

            return (

                "<h6>👋 Hello!</h6>"

                "<p>"
                "Welcome to the Healthcare AI Assistant."
                "</p>"

                "<p>"
                "I can help you with disease information, "
                "symptoms, diet, exercise, medicines, "
                "diagnosis, prevention and other healthcare "
                "information."
                "</p>"

                "<p>"
                "I can also answer questions about your "
                "Healthcare AI project."
                "</p>"

                "<p>"
                "Try asking:"
                "</p>"

                "<ul>"

                "<li>"
                "What are the symptoms of Typhoid?"
                "</li>"

                "<li>"
                "What is the diet for Diabetes?"
                "</li>"

                "<li>"
                "What is the objective of the project?"
                "</li>"

                "</ul>"

            )

        # ==================================================
        # THANK YOU
        # ==================================================

        if text in [
            "thanks",
            "thank you",
            "thankyou",
            "thx"
        ]:

            return (

                "<h6>😊 You're welcome!</h6>"

                "<p>"
                "Feel free to ask another healthcare "
                "or project-related question."
                "</p>"

            )

        # ==================================================
        # HELP
        # ==================================================

        if (
            text == "help"
            or "what can you do" in text
            or "what can i ask" in text
            or "how can you help" in text
        ):

            return self.get_help()

        # ==================================================
        # PROJECT QUESTIONS FIRST
        # ==================================================

        project_answer = (
            self.project_response(
                text
            )
        )

        if project_answer is not None:

            return project_answer

        # ==================================================
        # FIND DISEASE
        # ==================================================

        disease = self.find_disease(
            original_message
        )

        # ==================================================
        # FIND INDIVIDUAL SYMPTOM
        # ==================================================

        if disease is None:

            symptom = self.find_symptom(
                original_message
            )

            if symptom is not None:

                if (
                    "symptom" in text
                    or "meaning" in text
                    or "what is" in text
                    or "description" in text
                    or "explain" in text
                ):

                    description = (
                        self.get_symptom_description(
                            symptom
                        )
                    )

                    return (

                        "<h6>🩺 "
                        + self.safe_text(
                            symptom
                        )
                        + "</h6>"

                        "<p>"
                        + description
                        + "</p>"

                    )

        # ==================================================
        # DISEASE NOT FOUND
        # ==================================================

        if disease is None:

            return (

                "<h6>🔎 Information Not Found</h6>"

                "<p>"
                "I could not identify the disease "
                "or project topic in your question."
                "</p>"

                "<p>"
                "Please mention the disease name."
                "</p>"

                "<p>"
                "For example:"
                "</p>"

                "<ul>"

                "<li>"
                "What are the symptoms of Typhoid?"
                "</li>"

                "<li>"
                "What diet is recommended for Diabetes?"
                "</li>"

                "<li>"
                "What causes Dengue?"
                "</li>"

                "<li>"
                "What is the objective of the project?"
                "</li>"

                "</ul>"

            )

        # ==================================================
        # COMPLETE INFORMATION
        # ==================================================

        if (
            "complete information" in text
            or "all information" in text
            or "everything about" in text
            or "full information" in text
            or "full details" in text
            or "complete details" in text
        ):

            return self.get_complete_recommendation(
                disease
            )

        # ==================================================
        # SYMPTOMS
        # ==================================================

        if (
            "symptom" in text
            or "symptoms" in text
            or "signs" in text
            or "sign" in text
        ):

            symptoms_html = (
                self.get_disease_symptoms(
                    disease
                )
            )
            

            return (

                "<div class='chat-section'>"

                "<div class='chat-section-title'>"
                "🩺 Symptoms of "
                + self.safe_text(
                    disease
                )
                + "</div>"

                + symptoms_html

                +"</div>"

            )

        # ==================================================
        # DIET
        # ==================================================

        if (
            "diet" in text
            or "food" in text
            or "foods" in text
            or "eat" in text
            or "eating" in text
        ):

            return (

                "<h6>🥗 Diet for "
                + self.safe_text(
                    disease
                )
                + "</h6>"

                + self.get_diet(
                    disease
                )

            )

        # ==================================================
        # PRECAUTIONS
        # ==================================================

        if (
            "precaution" in text
            or "precautions" in text
            or "care should i take" in text
        ):

            return (

                "<h6>📝 Precautions for "
                + self.safe_text(
                    disease
                )
                + "</h6>"

                + self.get_precautions(
                    disease
                )

            )

        # ==================================================
        # CAUSES
        # ==================================================

        if (
            "cause" in text
            or "causes" in text
            or "why does" in text
            or "why do" in text
        ):

            return (

                "<h6>❓ Causes of "
                + self.safe_text(
                    disease
                )
                + "</h6>"

                "<p>"
                + self.get_causes(
                    disease
                )
                + "</p>"

            )

        # ==================================================
        # DIAGNOSIS
        # ==================================================

        if (
            "diagnosis" in text
            or "diagnose" in text
            or "diagnosed" in text
        ):

            return (

                "<h6>🔍 Diagnosis of "
                + self.safe_text(
                    disease
                )
                + "</h6>"

                "<p>"
                + self.get_diagnosis(
                    disease
                )
                + "</p>"

            )

        # ==================================================
        # LAB TESTS
        # ==================================================

        if (
            "lab test" in text
            or "lab tests" in text
            or "laboratory" in text
            or "blood test" in text
            or "test required" in text
            or "tests required" in text
        ):

            return (

                "<h6>🧪 Laboratory Tests for "
                + self.safe_text(
                    disease
                )
                + "</h6>"

                + self.get_lab_tests(
                    disease
                )

            )

        # ==================================================
        # RISK FACTORS
        # ==================================================

        if (
            "risk factor" in text
            or "risk factors" in text
            or "risk" in text
        ):

            return (

                "<h6>⚠️ Risk Factors for "
                + self.safe_text(
                    disease
                )
                + "</h6>"

                + self.get_risk_factors(
                    disease
                )

            )

        # ==================================================
        # COMPLICATIONS
        # ==================================================

        if (
            "complication" in text
            or "complications" in text
        ):

            return (

                "<h6>🩹 Complications of "
                + self.safe_text(
                    disease
                )
                + "</h6>"

                + self.get_complications(
                    disease
                )

            )

        # ==================================================
        # PREVENTION
        # ==================================================

        if (
            "prevention" in text
            or "prevent" in text
            or "how to prevent" in text
        ):

            return (

                "<h6>🛡️ Prevention of "
                + self.safe_text(
                    disease
                )
                + "</h6>"

                + self.get_prevention(
                    disease
                )

            )

        # ==================================================
        # TREATMENT
        # ==================================================

        if (
            "treatment" in text
            or "treat" in text
            or "how to treat" in text
        ):

            return (

                "<h6>💚 Treatment for "
                + self.safe_text(
                    disease
                )
                + "</h6>"

                "<p>"
                + self.get_treatment(
                    disease
                )
                + "</p>"

            )

        # ==================================================
        # SEVERITY
        # ==================================================

        if (
            "severity" in text
            or "severe" in text
            or "serious" in text
        ):

            return (

                "<h6>📊 Severity of "
                + self.safe_text(
                    disease
                )
                + "</h6>"

                "<p>"
                + self.get_severity(
                    disease
                )
                + "</p>"

            )

        # ==================================================
        # EMERGENCY
        # ==================================================

        if (
            "emergency" in text
            or "emergency level" in text
            or "urgent" in text
            or "emergency action" in text
        ):

            return (

                "<h6>🚨 Emergency Information for "
                + self.safe_text(
                    disease
                )
                + "</h6>"

                + self.get_emergency(
                    disease
                )

            )

        # ==================================================
        # EXERCISE
        # ==================================================

        if (
            "exercise" in text
            or "physical activity" in text
            or "workout" in text
        ):

            return (

                "<h6>🏃 Exercise for "
                + self.safe_text(
                    disease
                )
                + "</h6>"

                + self.get_exercise(
                    disease
                )

            )

        # ==================================================
        # MEDICINE
        # ==================================================

        if (
            "medicine" in text
            or "medicines" in text
            or "medication" in text
            or "medications" in text
            or "drug" in text
            or "drugs" in text
        ):

            return (

                "<h6>💊 Medicine Information for "
                + self.safe_text(
                    disease
                )
                + "</h6>"

                + self.get_medicine(
                    disease
                )

            )

        # ==================================================
        # SPECIALIST / DOCTOR
        # ==================================================

        if (
            "specialist" in text
            or "doctor" in text
            or "which doctor" in text
            or "consult" in text
        ):

            specialist = (
                self.get_specialist(
                    disease
                )
            )

            return (

                "<h6>👨‍⚕️ Specialist for "
                + self.safe_text(
                    disease
                )
                + "</h6>"

                "<p>"
                + specialist
                + "</p>"

            )

        # ==================================================
        # HEALTH TIPS
        # ==================================================

        if (
            "health tip" in text
            or "health tips" in text
            or text == "tip"
            or text == "tips"
            or "give me tips" in text
        ):

            tip = (
                self.get_health_tip(
                    disease
                )
            )

            return (

                "<h6>❤️ Health Tip for "
                + self.safe_text(
                    disease
                )
                + "</h6>"

                "<p>"
                + tip
                + "</p>"

            )

        # ==================================================
        # DESCRIPTION / OVERVIEW
        # ==================================================

        if (
            "description" in text
            or "describe" in text
            or "overview" in text
            or "what is " in text
            or "tell me about" in text
            or "information about" in text
            or text == self.normalize(
                disease
            )
        ):

            return self.get_disease_overview(
                disease
            )

        # ==================================================
        # DEFAULT
        # ==================================================

        return self.get_disease_overview(
            disease
        )
# ==========================================================
# Healthcare AI - Prediction Routes
# ==========================================================

from flask import (
    Blueprint,
    render_template,
    request,
    session,
    redirect,
    url_for,
    flash
)

from ml.predict import (
    predict_disease,
    symptoms
)

from services.recommendation_service import (
    RecommendationService
)

from services.history_service import (
    HistoryService
)


# ==========================================================
# Blueprint
# ==========================================================

prediction_bp = Blueprint(
    "prediction_bp",
    __name__
)


# ==========================================================
# Recommendation Service
# ==========================================================

recommendation_service = (
    RecommendationService()
)


# ==========================================================
# Symptoms Page
# ==========================================================

@prediction_bp.route(
    "/symptoms"
)
def symptoms_page():

    # ------------------------------------------------------
    # Login Check
    # ------------------------------------------------------

    if "user_id" not in session:

        return redirect(
            url_for(
                "auth_bp.login"
            )
        )

    # ------------------------------------------------------
    # Display Symptoms
    # ------------------------------------------------------

    return render_template(
        "symptoms.html",
        symptoms=sorted(
            symptoms
        )
    )


# ==========================================================
# Predict Disease
# ==========================================================

@prediction_bp.route(
    "/predict",
    methods=["POST"]
)
def predict():

    # ------------------------------------------------------
    # Login Check
    # ------------------------------------------------------

    if "user_id" not in session:

        return redirect(
            url_for(
                "auth_bp.login"
            )
        )

    # ======================================================
    # GET SELECTED SYMPTOMS
    # ======================================================

    selected = request.form.getlist(
        "symptoms"
    )

    # Remove empty values
    selected = [
        symptom.strip()
        for symptom in selected
        if symptom
        and symptom.strip()
    ]

    # ======================================================
    # MINIMUM SYMPTOM VALIDATION
    # ======================================================

    if len(selected) < 4:

        flash(
            "Please select at least 4 symptoms "
            "for better prediction accuracy.",
            "warning"
        )

        return redirect(
            url_for(
                "prediction_bp.symptoms_page"
            )
        )

    # ======================================================
    # AI PREDICTION
    # ======================================================

    try:

        disease, confidence, top_predictions = (
            predict_disease(
                selected
            )
        )

    except Exception as e:

        print(
            "[PREDICTION ERROR]",
            e
        )

        flash(
            "Unable to predict the disease. "
            "Please try again.",
            "danger"
        )

        return redirect(
            url_for(
                "prediction_bp.symptoms_page"
            )
        )

    # ======================================================
    # CLEAN PREDICTION VALUES
    # ======================================================

    disease = str(
        disease
    ).strip()

    try:

        confidence = float(
            confidence
        )

    except (
        TypeError,
        ValueError
    ):

        confidence = 0.0

    # ======================================================
    # SAVE LATEST PREDICTION
    # ======================================================

    session["last_disease"] = (
        disease
    )

    session["last_confidence"] = round(
        confidence,
        2
    )

    # ======================================================
    # GET RECOMMENDATION DATA
    # ======================================================

    try:

        recommendation_data = (
            recommendation_service
            .get_complete_recommendation(
                disease
            )
        )

    except Exception as e:

        print(
            "[RECOMMENDATION ERROR]",
            e
        )

        flash(
            "Disease prediction was successful, "
            "but some medical information could "
            "not be loaded.",
            "warning"
        )

        recommendation_data = {
            "description":
                "Description not available.",

            "causes":
                "Cause information not available.",

            "diagnosis":
                "Diagnosis information not available.",

            "lab_tests":
                "Laboratory information not available.",

            "risk_factors":
                "Risk-factor information not available.",

            "complications":
                "Complication information not available.",

            "prevention":
                [],

            "treatment":
                "Treatment information not available.",

            "severity": {
                "severity":
                    "Unknown",

                "emergency":
                    "Unknown"
            },

            "emergency": {
                "level":
                    "Unknown",

                "action":
                    "Consult a healthcare professional."
            },

            "precautions":
                [],

            "diet": {
                "recommended":
                    "Not Available",

                "avoid":
                    "Not Available"
            },

            "exercise": {
                "exercise":
                    "Not Available",

                "duration":
                    "Not Available"
            },

            "medicine": {
                "medicine":
                    "Consult Doctor",

                "type":
                    "-"
            },

            "specialist":
                "General Physician",

            "health_tip":
                "Stay Healthy."
        }

    # ======================================================
    # EXTRACT SEVERITY
    # ======================================================

    severity_data = (
        recommendation_data.get(
            "severity",
            {}
        )
    )

    if isinstance(
        severity_data,
        dict
    ):

        severity = (
            severity_data.get(
                "severity",
                "Unknown"
            )
        )

    else:

        severity = (
            str(
                severity_data
            )
            if severity_data
            else "Unknown"
        )

    # ======================================================
    # EXTRACT EMERGENCY DATA
    # ======================================================

    emergency_data = (
        recommendation_data.get(
            "emergency",
            {}
        )
    )

    if isinstance(
        emergency_data,
        dict
    ):

        emergency_level = (
            emergency_data.get(
                "level",
                "Unknown"
            )
        )

        recommended_action = (
            emergency_data.get(
                "action",
                "Consult a healthcare professional."
            )
        )

    else:

        emergency_level = (
            str(
                emergency_data
            )
            if emergency_data
            else "Unknown"
        )

        recommended_action = (
            "Consult a healthcare professional."
        )

    # ======================================================
    # SAVE PREDICTION HISTORY
    # ======================================================

    try:

        HistoryService.save_prediction(

            user_id=session[
                "user_id"
            ],

            disease_name=disease,

            confidence=confidence,

            symptoms=selected

        )

    except Exception as e:

        print(
            "[HISTORY ERROR]",
            e
        )

    # ======================================================
    # STORE DATA FOR PDF
    # ======================================================

    session["prediction_data"] = {

        # --------------------------------------------------
        # User Information
        # --------------------------------------------------

        "user_name":
            session.get(
                "user_name",
                ""
            ),

        "email":
            session.get(
                "email",
                ""
            ),

        "phone":
            session.get(
                "phone",
                ""
            ),

        "gender":
            session.get(
                "gender",
                ""
            ),

        "age":
            session.get(
                "age",
                ""
            ),

        # --------------------------------------------------
        # Prediction
        # --------------------------------------------------

        "disease":
            disease,

        "confidence":
            confidence,

        "top_predictions":
            top_predictions,

        "symptoms":
            selected,

        # --------------------------------------------------
        # Medical Information
        # --------------------------------------------------

        "description":
            recommendation_data.get(
                "description",
                "Description not available."
            ),

        "causes":
            recommendation_data.get(
                "causes",
                "Cause information not available."
            ),

        "diagnosis":
            recommendation_data.get(
                "diagnosis",
                "Diagnosis information not available."
            ),

        "lab_tests":
            recommendation_data.get(
                "lab_tests",
                "Laboratory information not available."
            ),

        "risk_factors":
            recommendation_data.get(
                "risk_factors",
                "Risk-factor information not available."
            ),

        "complications":
            recommendation_data.get(
                "complications",
                "Complication information not available."
            ),

        "prevention":
            recommendation_data.get(
                "prevention",
                []
            ),

        "treatment":
            recommendation_data.get(
                "treatment",
                "Treatment information not available."
            ),

        # --------------------------------------------------
        # Severity
        # --------------------------------------------------

        "severity":
            severity,

        # --------------------------------------------------
        # Emergency
        #
        # Keep both formats so existing PDF code can
        # continue to work.
        # --------------------------------------------------

        "emergency":
            emergency_level,

        "emergency_level":
            emergency_level,

        "recommended_action":
            recommended_action,

        # --------------------------------------------------
        # Other Information
        # --------------------------------------------------

        "precautions":
            recommendation_data.get(
                "precautions",
                []
            ),

        "diet":
            recommendation_data.get(
                "diet",
                {
                    "recommended":
                        "Not Available",

                    "avoid":
                        "Not Available"
                }
            ),

        "exercise":
            recommendation_data.get(
                "exercise",
                {
                    "exercise":
                        "Not Available",

                    "duration":
                        "Not Available"
                }
            ),

        "medicine":
            recommendation_data.get(
                "medicine",
                {
                    "medicine":
                        "Consult Doctor",

                    "type":
                        "-"
                }
            ),

        "specialist":
            recommendation_data.get(
                "specialist",
                "General Physician"
            ),

        "health_tip":
            recommendation_data.get(
                "health_tip",
                "Stay Healthy."
            )
    }

    # ======================================================
    # DEBUG INFORMATION
    # ======================================================

    print("\n")
    print("=" * 70)
    print("PREDICTION COMPLETED")
    print("=" * 70)

    print(
        "Disease:",
        disease
    )

    print(
        "Confidence:",
        confidence
    )

    print(
        "Selected Symptoms:",
        selected
    )

    print(
        "Severity:",
        severity
    )

    print(
        "Emergency Level:",
        emergency_level
    )

    print(
        "Recommended Action:",
        recommended_action
    )

    print(
        "Top Predictions:"
    )

    print(
        top_predictions
    )

    print("=" * 70)

    # ======================================================
    # RESULT PAGE
    # ======================================================

    return render_template(

        "prediction_result.html",

        # --------------------------------------------------
        # Prediction
        # --------------------------------------------------

        disease=disease,

        confidence=confidence,

        top_predictions=top_predictions,

        selected_symptoms=selected,

        # --------------------------------------------------
        # Medical Information
        # --------------------------------------------------

        description=
            recommendation_data.get(
                "description",
                "Description not available."
            ),

        causes=
            recommendation_data.get(
                "causes",
                "Cause information not available."
            ),

        diagnosis=
            recommendation_data.get(
                "diagnosis",
                "Diagnosis information not available."
            ),

        lab_tests=
            recommendation_data.get(
                "lab_tests",
                "Laboratory information not available."
            ),

        risk_factors=
            recommendation_data.get(
                "risk_factors",
                "Risk-factor information not available."
            ),

        complications=
            recommendation_data.get(
                "complications",
                "Complication information not available."
            ),

        prevention=
            recommendation_data.get(
                "prevention",
                []
            ),

        treatment=
            recommendation_data.get(
                "treatment",
                "Treatment information not available."
            ),

        # --------------------------------------------------
        # Severity
        # --------------------------------------------------

        severity=severity,

        # --------------------------------------------------
        # Emergency
        # --------------------------------------------------

        emergency=emergency_level,

        emergency_level=emergency_level,

        recommended_action=recommended_action,

        # --------------------------------------------------
        # Other Information
        # --------------------------------------------------

        precautions=
            recommendation_data.get(
                "precautions",
                []
            ),

        diet=
            recommendation_data.get(
                "diet",
                {
                    "recommended":
                        "Not Available",

                    "avoid":
                        "Not Available"
                }
            ),

        exercise=
            recommendation_data.get(
                "exercise",
                {
                    "exercise":
                        "Not Available",

                    "duration":
                        "Not Available"
                }
            ),

        medicine=
            recommendation_data.get(
                "medicine",
                {
                    "medicine":
                        "Consult Doctor",

                    "type":
                        "-"
                }
            ),

        specialist=
            recommendation_data.get(
                "specialist",
                "General Physician"
            ),

        health_tip=
            recommendation_data.get(
                "health_tip",
                "Stay Healthy."
            )
    )
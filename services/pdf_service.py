from io import BytesIO
from pathlib import Path
import datetime
import html

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch

from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    Image,
    PageBreak
)


# ==========================================================
# SAFE TEXT CONVERTER
# ==========================================================

def safe_text(value):
    """
    Convert any value into a ReportLab-safe string.

    Supports:
        - strings
        - lists
        - dictionaries
        - numbers
        - None
    """

    # ------------------------------------------------------
    # None
    # ------------------------------------------------------

    if value is None:

        return "Not Available"

    # ------------------------------------------------------
    # LIST
    # ------------------------------------------------------

    if isinstance(value, list):

        items = []

        for item in value:

            if item is None:
                continue

            item = str(item).strip()

            if not item:
                continue

            items.append(
                "• " + html.escape(item)
            )

        if not items:

            return "Not Available"

        return "<br/>".join(items)

    # ------------------------------------------------------
    # DICTIONARY
    # ------------------------------------------------------

    if isinstance(value, dict):

        if not value:

            return "Not Available"

        parts = []

        for key, item in value.items():

            if item is None:
                continue

            key_text = (
                str(key)
                .replace("_", " ")
                .title()
            )

            # ----------------------------------------------
            # Dictionary value is a list
            # ----------------------------------------------

            if isinstance(item, list):

                list_items = []

                for x in item:

                    if x is None:
                        continue

                    x = str(x).strip()

                    if x:

                        list_items.append(
                            "• " + html.escape(x)
                        )

                item_text = "<br/>".join(
                    list_items
                )

            else:

                item_text = html.escape(
                    str(item).strip()
                )

            if item_text:

                parts.append(
                    f"<b>{html.escape(key_text)}:</b> "
                    f"{item_text}"
                )

        if not parts:

            return "Not Available"

        return "<br/>".join(parts)

    # ------------------------------------------------------
    # STRING / NUMBER / OTHER
    # ------------------------------------------------------

    return html.escape(
        str(value)
    )


# ==========================================================
# PDF SERVICE
# ==========================================================

class PDFService:

    @staticmethod
    def generate_report(data):

        # ==================================================
        # PDF DOCUMENT
        # ==================================================

        buffer = BytesIO()

        doc = SimpleDocTemplate(

            buffer,

            rightMargin=30,

            leftMargin=30,

            topMargin=30,

            bottomMargin=30
        )

        # ==================================================
        # STYLES
        # ==================================================

        styles = getSampleStyleSheet()

        title = styles["Heading1"]

        title.alignment = TA_CENTER

        title.textColor = colors.darkblue


        heading = styles["Heading2"]

        heading.textColor = colors.darkgreen


        subheading = styles["Heading3"]

        subheading.textColor = colors.darkred


        body = styles["BodyText"]

        body.alignment = TA_LEFT


        story = []

        # ==================================================
        # LOGO
        # ==================================================

        logo = (

            Path(__file__).resolve().parent.parent

            / "static"

            / "images"

            / "healthcare_ai_logo.png"

        )

        if logo.exists():

            img = Image(
                str(logo)
            )

            img.drawWidth = 1.4 * inch

            img.drawHeight = 1.4 * inch

            img.hAlign = "CENTER"

            story.append(img)

        story.append(
            Spacer(1, 10)
        )

        # ==================================================
        # TITLE
        # ==================================================

        story.append(

            Paragraph(

                "<b><font size='24'>Healthcare AI</font></b>",

                title

            )

        )

        story.append(

            Paragraph(

                "<b>Artificial Intelligence Disease "
                "Prediction Report</b>",

                heading

            )

        )

        story.append(
            Spacer(1, 15)
        )

        # ==================================================
        # REPORT DETAILS
        # ==================================================

        report_id = (

            "HCAI-"

            + datetime.datetime.now().strftime(
                "%Y%m%d%H%M%S"
            )

        )

        story.append(

            Paragraph(

                f"<b>Report ID :</b> "
                f"{html.escape(report_id)}",

                body

            )

        )

        generated_time = (

            datetime.datetime.now().strftime(
                "%d-%b-%Y %I:%M %p"
            )

        )

        story.append(

            Paragraph(

                f"<b>Generated :</b> "
                f"{html.escape(generated_time)}",

                body

            )

        )

        story.append(
            Spacer(1, 15)
        )

        # ==================================================
        # PATIENT DETAILS TABLE
        # ==================================================

        patient_data = [

            [
                "Patient Name",
                str(data.get("user_name", ""))
            ],

            [
                "Email",
                str(data.get("email", ""))
            ],

            [
                "Phone",
                str(data.get("phone", ""))
            ],

            [
                "Gender",
                str(data.get("gender", ""))
            ],

            [
                "Age",
                str(data.get("age", ""))
            ],

            [
                "Predicted Disease",
                str(data.get("disease", ""))
            ],

            [
                "Prediction Confidence",
                f"{round(float(data.get('confidence', 0)), 2)}%"
            ]

        ]

        # Escape table text
        patient_data = [

            [
                html.escape(str(cell))
                for cell in row
            ]

            for row in patient_data

        ]

        patient_table = Table(

            patient_data,

            colWidths=[
                180,
                300
            ]

        )

        patient_table.setStyle(

            TableStyle([

                (
                    "GRID",
                    (0, 0),
                    (-1, -1),
                    1,
                    colors.grey
                ),

                (
                    "BACKGROUND",
                    (0, 0),
                    (0, -1),
                    colors.HexColor("#D6EEF8")
                ),

                (
                    "BACKGROUND",
                    (1, 0),
                    (1, -1),
                    colors.whitesmoke
                ),

                (
                    "FONTNAME",
                    (0, 0),
                    (-1, -1),
                    "Helvetica-Bold"
                ),

                (
                    "FONTSIZE",
                    (0, 0),
                    (-1, -1),
                    11
                ),

                (
                    "BOTTOMPADDING",
                    (0, 0),
                    (-1, -1),
                    10
                ),

                (
                    "TOPPADDING",
                    (0, 0),
                    (-1, -1),
                    10
                ),

                (
                    "VALIGN",
                    (0, 0),
                    (-1, -1),
                    "MIDDLE"
                )

            ])

        )

        story.append(
            patient_table
        )

        story.append(
            Spacer(1, 20)
        )

        # ==================================================
        # PREDICTION STATUS
        # ==================================================

        try:

            confidence = float(
                data.get(
                    "confidence",
                    0
                )
            )

        except:

            confidence = 0


        disease = str(
            data.get(
                "disease",
                "the predicted disease"
            )
        )

        disease_html = html.escape(
            disease
        )

        # --------------------------------------------------
        # Very High
        # --------------------------------------------------

        if confidence >= 90:

            status_color = "green"

            status = (
                "VERY HIGH CONFIDENCE"
            )

            message = f"""
            The selected symptoms strongly match
            <b>{disease_html}</b>.

            The prediction is highly reliable based on
            the available symptom data.

            Please consult a healthcare professional
            for confirmation and treatment.
            """

        # --------------------------------------------------
        # High
        # --------------------------------------------------

        elif confidence >= 75:

            status_color = "darkgreen"

            status = (
                "HIGH CONFIDENCE"
            )

            message = f"""
            The selected symptoms are highly consistent
            with <b>{disease_html}</b>.

            The prediction is reliable, but medical
            confirmation is still recommended.
            """

        # --------------------------------------------------
        # Moderate
        # --------------------------------------------------

        elif confidence >= 50:

            status_color = "orange"

            status = (
                "MODERATE CONFIDENCE"
            )

            message = f"""
            The selected symptoms partially match
            <b>{disease_html}</b>.

            Several diseases may share similar symptoms.

            Consider providing additional symptoms or
            consulting a doctor.
            """

        # --------------------------------------------------
        # Low
        # --------------------------------------------------

        else:

            status_color = "red"

            status = (
                "LOW CONFIDENCE"
            )

            message = """
            The selected symptoms match multiple diseases,
            therefore the prediction confidence is low.

            <br/><br/>

            <b>Recommendation:</b>

            Please provide additional symptoms to improve
            prediction accuracy or consult a qualified
            healthcare professional for proper diagnosis
            and laboratory investigations.
            """

        story.append(

            Paragraph(
                "<b>Prediction Status</b>",
                heading
            )

        )

        story.append(

            Paragraph(

                f"<font color='{status_color}'>"
                f"<b>{status}</b>"
                f"</font>",

                body

            )

        )

        story.append(

            Paragraph(

                f"<b>Confidence :</b> "
                f"{round(confidence, 2)}%",

                body

            )

        )

        story.append(
            Spacer(1, 6)
        )

        story.append(

            Paragraph(
                message,
                body
            )

        )

        story.append(
            Spacer(1, 20)
        )

        # ==================================================
        # TOP 5 DISEASE PREDICTIONS
        # ==================================================

        story.append(

            Paragraph(
                "<b>Top 5 Disease Predictions</b>",
                heading
            )

        )

        top_predictions = data.get(
            "top_predictions",
            []
        )

        prediction_table = [

            [
                "Rank",
                "Disease",
                "Confidence"
            ]

        ]

        if isinstance(
            top_predictions,
            list
        ):

            for index, item in enumerate(
                top_predictions,
                start=1
            ):

                if not isinstance(
                    item,
                    dict
                ):

                    continue

                prediction_disease = str(
                    item.get(
                        "disease",
                        ""
                    )
                )

                try:

                    prediction_confidence = float(
                        item.get(
                            "confidence",
                            0
                        )
                    )

                except:

                    prediction_confidence = 0

                prediction_table.append(

                    [

                        str(index),

                        prediction_disease,

                        f"{round(prediction_confidence, 2)}%"

                    ]

                )

        if len(prediction_table) == 1:

            prediction_table.append(

                [
                    "-",
                    "No additional predictions available",
                    "-"
                ]

            )

        prediction_table = [

            [
                html.escape(str(cell))
                for cell in row
            ]

            for row in prediction_table

        ]

        predictionTable = Table(

            prediction_table,

            colWidths=[
                60,
                250,
                150
            ]

        )

        predictionTable.setStyle(

            TableStyle([

                (
                    "GRID",
                    (0, 0),
                    (-1, -1),
                    1,
                    colors.black
                ),

                (
                    "BACKGROUND",
                    (0, 0),
                    (-1, 0),
                    colors.darkblue
                ),

                (
                    "TEXTCOLOR",
                    (0, 0),
                    (-1, 0),
                    colors.white
                ),

                (
                    "BACKGROUND",
                    (0, 1),
                    (-1, -1),
                    colors.beige
                ),

                (
                    "FONTNAME",
                    (0, 0),
                    (-1, 0),
                    "Helvetica-Bold"
                ),

                (
                    "ALIGN",
                    (0, 0),
                    (-1, -1),
                    "CENTER"
                ),

                (
                    "BOTTOMPADDING",
                    (0, 0),
                    (-1, -1),
                    8
                )

            ])

        )

        story.append(
            predictionTable
        )

        story.append(
            Spacer(1, 20)
        )

        # ==================================================
        # SELECTED SYMPTOMS
        # ==================================================

        story.append(

            Paragraph(
                "<b>Selected Symptoms</b>",
                heading
            )

        )

        symptoms = data.get(
            "symptoms",
            []
        )

        if isinstance(
            symptoms,
            list
        ) and symptoms:

            symptom_items = []

            for symptom in symptoms:

                symptom = str(
                    symptom
                ).replace(
                    "_",
                    " "
                ).title()

                symptom_items.append(
                    "✓ " + html.escape(symptom)
                )

            symptom_text = "<br/>".join(
                symptom_items
            )

        elif symptoms:

            symptom_text = safe_text(
                symptoms
            )

        else:

            symptom_text = "No Symptoms"

        story.append(

            Paragraph(
                symptom_text,
                body
            )

        )

        story.append(
            Spacer(1, 20)
        )

        # ==================================================
        # DISEASE DESCRIPTION
        # ==================================================

        story.append(

            Paragraph(
                "<b>Disease Description</b>",
                heading
            )

        )

        story.append(

            Paragraph(

                safe_text(
                    data.get(
                        "description",
                        "Not Available"
                    )
                ),

                body

            )

        )

        story.append(
            Spacer(1, 15)
        )

        # ==================================================
        # CAUSES
        # ==================================================

        story.append(

            Paragraph(
                "<b>Causes</b>",
                heading
            )

        )

        story.append(

            Paragraph(

                safe_text(
                    data.get(
                        "causes",
                        "Not Available"
                    )
                ),

                body

            )

        )

        story.append(
            Spacer(1, 15)
        )

        # ==================================================
        # DIAGNOSIS
        # ==================================================

        story.append(

            Paragraph(
                "<b>Diagnosis</b>",
                heading
            )

        )

        story.append(

            Paragraph(

                safe_text(
                    data.get(
                        "diagnosis",
                        "Not Available"
                    )
                ),

                body

            )

        )

        story.append(
            Spacer(1, 15)
        )

        # ==================================================
        # LABORATORY TESTS
        # ==================================================

        story.append(

            Paragraph(
                "<b>Laboratory Tests</b>",
                heading
            )

        )

        story.append(

            Paragraph(

                safe_text(
                    data.get(
                        "lab_tests",
                        "Not Available"
                    )
                ),

                body

            )

        )

        story.append(
            Spacer(1, 15)
        )

        # ==================================================
        # RISK FACTORS
        # ==================================================

        story.append(

            Paragraph(
                "<b>Risk Factors</b>",
                heading
            )

        )

        story.append(

            Paragraph(

                safe_text(
                    data.get(
                        "risk_factors",
                        "Not Available"
                    )
                ),

                body

            )

        )

        story.append(
            Spacer(1, 15)
        )

        # ==================================================
        # COMPLICATIONS
        # ==================================================

        story.append(

            Paragraph(
                "<b>Possible Complications</b>",
                heading
            )

        )

        story.append(

            Paragraph(

                safe_text(
                    data.get(
                        "complications",
                        "Not Available"
                    )
                ),

                body

            )

        )

        story.append(
            Spacer(1, 15)
        )

        # ==================================================
        # PAGE BREAK
        # ==================================================

        story.append(
            PageBreak()
        )

        # ==================================================
        # PREVENTION
        # ==================================================

        story.append(

            Paragraph(
                "<b>Prevention</b>",
                heading
            )

        )

        prevention = data.get(
            "prevention",
            "Not Available"
        )

        story.append(

            Paragraph(
                safe_text(prevention),
                body
            )

        )

        story.append(
            Spacer(1, 15)
        )

        # ==================================================
        # TREATMENT
        # ==================================================

        story.append(

            Paragraph(
                "<b>Treatment</b>",
                heading
            )

        )

        treatment = data.get(
            "treatment",
            "Not Available"
        )

        story.append(

            Paragraph(
                safe_text(treatment),
                body
            )

        )

        story.append(
            Spacer(1, 15)
        )

        # ==================================================
        # SEVERITY
        # ==================================================

        story.append(

            Paragraph(
                "<b>Severity Assessment</b>",
                heading
            )

        )

        severity_data = data.get(
            "severity",
            {}
        )

        # --------------------------------------------------
        # Severity can be dictionary or string
        # --------------------------------------------------

        if isinstance(
            severity_data,
            dict
        ):

            severity_value = severity_data.get(
                "severity",
                "Unknown"
            )

        else:

            severity_value = severity_data

        story.append(

            Paragraph(

                f"<b>Severity :</b> "
                f"{safe_text(severity_value)}",

                body

            )

        )

        story.append(
            Spacer(1, 8)
        )

        # ==================================================
        # EMERGENCY LEVEL
        # ==================================================

        emergency = data.get(
            "emergency",
            {}
        )

        if isinstance(
            emergency,
            dict
        ):

            emergency_level = emergency.get(
                "level",
                "Unknown"
            )

            recommended_action = emergency.get(
                "action",
                "Consult a healthcare professional."
            )

        else:

            emergency_level = emergency

            recommended_action = (
                "Consult a healthcare professional."
            )

        emergency_level = str(
            emergency_level
        ).strip()

        recommended_action = str(
            recommended_action
        ).strip()

        # --------------------------------------------------
        # Critical emergency levels
        # --------------------------------------------------

        critical_levels = {

            "critical",
            "high",
            "immediate",
            "emergency"

        }

        if (
            emergency_level.lower()
            in critical_levels
        ):

            emergency_text = f"""

            <font color='red'>
            <b>⚠ IMMEDIATE MEDICAL ATTENTION
            MAY BE REQUIRED</b>
            </font>

            <br/><br/>

            <b>Emergency Level:</b>
            {html.escape(emergency_level)}

            <br/><br/>

            <b>Recommended Action:</b>
            {html.escape(recommended_action)}

            """

        else:

            emergency_text = f"""

            <font color='green'>
            <b>EMERGENCY LEVEL INFORMATION</b>
            </font>

            <br/><br/>

            <b>Emergency Level:</b>
            {html.escape(emergency_level)}

            <br/><br/>

            <b>Recommended Action:</b>
            {html.escape(recommended_action)}

            """

        story.append(

            Paragraph(
                emergency_text,
                body
            )

        )

        story.append(
            Spacer(1, 15)
        )

        # ==================================================
        # PRECAUTIONS
        # ==================================================

        story.append(

            Paragraph(
                "<b>Precautions</b>",
                heading
            )

        )

        precautions = data.get(
            "precautions",
            []
        )

        if isinstance(
            precautions,
            list
        ):

            precaution_items = []

            for precaution in precautions:

                if precaution is None:
                    continue

                precaution = str(
                    precaution
                ).strip()

                if precaution:

                    precaution_items.append(
                        "• "
                        + html.escape(
                            precaution
                        )
                    )

            if precaution_items:

                precaution_text = (
                    "<br/>".join(
                        precaution_items
                    )
                )

            else:

                precaution_text = (
                    "Not Available"
                )

        else:

            precaution_text = safe_text(
                precautions
            )

        story.append(

            Paragraph(
                precaution_text,
                body
            )

        )

        story.append(
            Spacer(1, 15)
        )

        # ==================================================
        # DIET
        # ==================================================

        story.append(

            Paragraph(
                "<b>Recommended Diet</b>",
                heading
            )

        )

        diet = data.get(
            "diet",
            {}
        )

        if isinstance(
            diet,
            dict
        ):

            recommended_foods = safe_text(

                diet.get(
                    "recommended",
                    "Not Available"
                )

            )

            foods_to_avoid = safe_text(

                diet.get(
                    "avoid",
                    "Not Available"
                )

            )

        else:

            recommended_foods = safe_text(
                diet
            )

            foods_to_avoid = (
                "Not Available"
            )

        diet_text = f"""

        <b>Recommended Foods:</b><br/>

        {recommended_foods}

        <br/><br/>

        <b>Foods To Avoid:</b><br/>

        {foods_to_avoid}

        """

        story.append(

            Paragraph(
                diet_text,
                body
            )

        )

        story.append(
            Spacer(1, 15)
        )

        # ==================================================
        # EXERCISE
        # ==================================================

        story.append(

            Paragraph(
                "<b>Exercise Recommendation</b>",
                heading
            )

        )

        exercise = data.get(
            "exercise",
            {}
        )

        if isinstance(
            exercise,
            dict
        ):

            exercise_value = safe_text(

                exercise.get(
                    "exercise",
                    "Not Available"
                )

            )

            duration_value = safe_text(

                exercise.get(
                    "duration",
                    "Not Available"
                )

            )

        else:

            exercise_value = safe_text(
                exercise
            )

            duration_value = (
                "Not Available"
            )

        exercise_text = f"""

        <b>Exercise:</b><br/>

        {exercise_value}

        <br/><br/>

        <b>Duration:</b><br/>

        {duration_value}

        """

        story.append(

            Paragraph(
                exercise_text,
                body
            )

        )

        story.append(
            Spacer(1, 15)
        )

        # ==================================================
        # MEDICINE
        # ==================================================

        story.append(

            Paragraph(
                "<b>Medicine Recommendation</b>",
                heading
            )

        )

        medicine = data.get(
            "medicine",
            {}
        )

        if isinstance(
            medicine,
            dict
        ):

            medicine_value = safe_text(

                medicine.get(
                    "medicine",
                    "Consult Doctor"
                )

            )

            medicine_type = safe_text(

                medicine.get(
                    "type",
                    "Not Available"
                )

            )

        else:

            medicine_value = safe_text(
                medicine
            )

            medicine_type = (
                "Not Available"
            )

        medicine_text = f"""

        <b>Medicine:</b><br/>

        {medicine_value}

        <br/><br/>

        <b>Medicine Type:</b><br/>

        {medicine_type}

        """

        story.append(

            Paragraph(
                medicine_text,
                body
            )

        )

        story.append(
            Spacer(1, 15)
        )

        # ==================================================
        # DOCTOR SPECIALIST
        # ==================================================

        story.append(

            Paragraph(
                "<b>Recommended Doctor Specialist</b>",
                heading
            )

        )

        specialist = data.get(
            "specialist",
            "General Physician"
        )

        story.append(

            Paragraph(

                safe_text(
                    specialist
                ),

                body

            )

        )

        story.append(
            Spacer(1, 15)
        )

        # ==================================================
        # HEALTH TIP
        # ==================================================

        story.append(

            Paragraph(
                "<b>Daily Health Tip</b>",
                heading
            )

        )

        health_tip = data.get(
            "health_tip",
            "Stay Healthy."
        )

        story.append(

            Paragraph(

                safe_text(
                    health_tip
                ),

                body

            )

        )

        story.append(
            Spacer(1, 20)
        )

        # ==================================================
        # MEDICAL DISCLAIMER
        # ==================================================

        disclaimer = """

        <font color='red'>
        <b>Medical Disclaimer</b>
        </font>

        <br/><br/>

        This report has been generated using an Artificial
        Intelligence disease prediction model.

        The prediction is intended only for educational and
        informational purposes and must NOT be considered
        as a confirmed medical diagnosis.

        Always consult a qualified medical professional
        before taking any medication or making healthcare
        decisions.

        In case of severe symptoms or emergency conditions,
        immediately visit the nearest hospital.

        """

        story.append(

            Paragraph(
                disclaimer,
                body
            )

        )

        story.append(
            Spacer(1, 25)
        )

        # ==================================================
        # FOOTER
        # ==================================================

        story.append(

            Paragraph(
                "<b>Generated By</b>",
                heading
            )

        )

        story.append(

            Paragraph(

                "Healthcare AI Disease Prediction System",

                body

            )

        )

        story.append(

            Paragraph(

                "Python | Flask | Oracle Database | "
                "Machine Learning",

                body

            )

        )

        story.append(

            Paragraph(
                "© 2026 Healthcare AI",
                body
            )

        )

        # ==================================================
        # BUILD PDF
        # ==================================================

        doc.build(
            story
        )

        buffer.seek(0)

        return buffer
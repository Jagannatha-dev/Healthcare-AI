from routes.admin import admin_bp

from services.chatbot_service import ChatbotService
from services.pdf_service import PDFService
from services.profile_service import ProfileService
from services.history_service import HistoryService

from routes.prediction import prediction_bp
from routes.auth import auth_bp

from flask import (
    Flask,
    render_template,
    session,
    redirect,
    url_for,
    request,
    flash,
    jsonify,
    send_file
)

from config import SECRET_KEY


# ==========================================================
# CREATE FLASK APPLICATION
# ==========================================================

app = Flask(__name__)


# ==========================================================
# AI CHATBOT SERVICE
# ==========================================================

chatbot_service = ChatbotService()


# ==========================================================
# CONFIGURATION
# ==========================================================

app.config["SECRET_KEY"] = SECRET_KEY


# ==========================================================
# REGISTER BLUEPRINTS
# ==========================================================

app.register_blueprint(auth_bp)

app.register_blueprint(prediction_bp)

app.register_blueprint(admin_bp)


# ==========================================================
# HOME
# ==========================================================

@app.route("/")
def home():

    return render_template(
        "index.html"
    )


# ==========================================================
# DASHBOARD
# ==========================================================

@app.route("/dashboard")
def dashboard():

    # ------------------------------------------
    # Check Login
    # ------------------------------------------

    if "user_id" not in session:

        return redirect(
            url_for("auth_bp.login")
        )


    # ------------------------------------------
    # Get Logged-in User ID
    # ------------------------------------------

    user_id = session["user_id"]


    # ------------------------------------------
    # Get Latest Prediction From Database
    # ------------------------------------------

    latest_prediction = (
        HistoryService.get_latest_prediction(
            user_id
        )
    )


    # ------------------------------------------
    # Safety Fallback
    # ------------------------------------------

    if latest_prediction is None:

        latest_prediction = {

            "disease": None,

            "confidence": None,

            "symptoms": "",

            "date": None

        }


    # ------------------------------------------
    # Render Dashboard
    # ------------------------------------------

    return render_template(

        "dashboard.html",

        user_name=session.get(
            "user_name",
            ""
        ),

        latest_prediction=latest_prediction

    )


# ==========================================================
# PREDICTION HISTORY
# ==========================================================

@app.route("/history")
def history():

    # ------------------------------------------
    # Check Login
    # ------------------------------------------

    if "user_id" not in session:

        return redirect(
            url_for("auth_bp.login")
        )

    # ------------------------------------------
    # Get Current User History
    # ------------------------------------------

    history = HistoryService.get_history(
        session["user_id"]
    )

    # ------------------------------------------
    # Render History Page
    # ------------------------------------------

    return render_template(
        "history.html",
        history=history
    )


# ==========================================================
# VIEW INDIVIDUAL PREDICTION
# ==========================================================

@app.route("/history/<int:history_id>")
def view_prediction(history_id):

    # ------------------------------------------
    # Check Login
    # ------------------------------------------

    if "user_id" not in session:

        return redirect(
            url_for("auth_bp.login")
        )

    # ------------------------------------------
    # Get Logged-in User ID
    # ------------------------------------------

    user_id = session["user_id"]

    # ------------------------------------------
    # Get Selected Prediction
    # ------------------------------------------

    prediction = HistoryService.get_prediction_by_id(
        user_id,
        history_id
    )

    # ------------------------------------------
    # Prediction Not Found
    # ------------------------------------------

    if prediction is None:

        flash(
            "Prediction not found.",
            "warning"
        )

        return redirect(
            url_for("history")
        )

    # ------------------------------------------
    # Display Prediction
    # ------------------------------------------

    return render_template(
    "prediction_history_detail.html",
    prediction=prediction
)

# ==========================================================
# PROFILE
# ==========================================================

@app.route("/profile")
def profile():

    # ------------------------------------------
    # Check Login
    # ------------------------------------------

    if "user_id" not in session:

        return redirect(
            url_for("auth_bp.login")
        )


    # ------------------------------------------
    # Get Profile
    # ------------------------------------------

    profile = ProfileService.get_profile(

        session["user_id"]

    )


    if profile is None:

        flash(
            "Unable to load profile.",
            "danger"
        )

        return redirect(
            url_for("dashboard")
        )


    # ------------------------------------------
    # Get Total Predictions
    # ------------------------------------------

    total_predictions = (
        ProfileService.get_total_predictions(
            session["user_id"]
        )
    )


    # ------------------------------------------
    # Render Profile
    # ------------------------------------------

    return render_template(

        "profile.html",

        user_name=profile[0],

        email=profile[1],

        phone=profile[2],

        gender=profile[3],

        age=profile[4],

        joined=profile[5],

        total_predictions=total_predictions

    )


# ==========================================================
# EDIT PROFILE
# ==========================================================

@app.route(
    "/profile/edit",
    methods=["GET", "POST"]
)
def edit_profile():

    # ------------------------------------------
    # Check Login
    # ------------------------------------------

    if "user_id" not in session:

        return redirect(
            url_for("auth_bp.login")
        )


    # ------------------------------------------
    # Update Profile
    # ------------------------------------------

    if request.method == "POST":

        full_name = request.form[
            "full_name"
        ]

        phone = request.form[
            "phone"
        ]

        gender = request.form[
            "gender"
        ]

        age = request.form[
            "age"
        ]


        ProfileService.update_profile(

            session["user_id"],

            full_name,

            phone,

            gender,

            age

        )


        # --------------------------------------
        # Update Session Name
        # --------------------------------------

        session["user_name"] = full_name


        flash(
            "Profile updated successfully.",
            "success"
        )


        return redirect(
            url_for("profile")
        )


    # ------------------------------------------
    # Get Existing Profile
    # ------------------------------------------

    profile = ProfileService.get_profile(

        session["user_id"]

    )


    return render_template(

        "edit_profile.html",

        profile=profile

    )


# ==========================================================
# CHANGE PASSWORD
# ==========================================================

@app.route(
    "/change-password",
    methods=["GET", "POST"]
)
def change_password():

    # ------------------------------------------
    # Check Login
    # ------------------------------------------

    if "user_id" not in session:

        return redirect(
            url_for("auth_bp.login")
        )


    # ------------------------------------------
    # Change Password
    # ------------------------------------------

    if request.method == "POST":

        current_password = request.form[
            "current_password"
        ]

        new_password = request.form[
            "new_password"
        ]

        confirm_password = request.form[
            "confirm_password"
        ]


        # --------------------------------------
        # Confirm Password
        # --------------------------------------

        if new_password != confirm_password:

            flash(
                "New passwords do not match.",
                "danger"
            )

            return redirect(
                url_for("change_password")
            )


        # --------------------------------------
        # Update Password
        # --------------------------------------

        success, message = (
            ProfileService.change_password(

                session["user_id"],

                current_password,

                new_password

            )
        )


        if success:

            flash(
                message,
                "success"
            )

            return redirect(
                url_for("profile")
            )

        else:

            flash(
                message,
                "danger"
            )


    return render_template(
        "change_password.html"
    )


# ==========================================================
# DOWNLOAD PDF
# ==========================================================

@app.route("/download-pdf")
def download_pdf():

    # ------------------------------------------
    # Check Login
    # ------------------------------------------

    if "user_id" not in session:

        return redirect(
            url_for("auth_bp.login")
        )


    # ------------------------------------------
    # Get Prediction Data
    # ------------------------------------------

    prediction_data = session.get(
        "prediction_data"
    )


    if prediction_data is None:

        flash(
            "No prediction available to download.",
            "warning"
        )

        return redirect(
            url_for("dashboard")
        )


    # ------------------------------------------
    # Get User Profile
    # ------------------------------------------

    profile = ProfileService.get_profile(

        session["user_id"]

    )


    if profile:

        prediction_data["user_name"] = profile[0]

        prediction_data["email"] = profile[1]

        prediction_data["phone"] = profile[2]

        prediction_data["gender"] = profile[3]

        prediction_data["age"] = profile[4]


    # ------------------------------------------
    # Generate PDF
    # ------------------------------------------

    pdf = PDFService.generate_report(
        prediction_data
    )


    return send_file(

        pdf,

        as_attachment=True,

        download_name=(
            "Healthcare_AI_Report.pdf"
        ),

        mimetype="application/pdf"

    )


# ==========================================================
# CHATBOT PAGE
# ==========================================================

@app.route("/chatbot")
def chatbot_page():

    # ------------------------------------------
    # Check Login
    # ------------------------------------------

    if "user_id" not in session:

        return redirect(
            url_for("auth_bp.login")
        )


    return render_template(

        "chatbot.html",

        user_name=session.get(
            "user_name"
        )

    )


# ==========================================================
# CHAT API
# ==========================================================

@app.route(
    "/chat",
    methods=["POST"]
)
def chat():

    # ------------------------------------------
    # Check Login
    # ------------------------------------------

    if "user_id" not in session:

        return jsonify({

            "reply":
            "Please login first."

        })


    # ------------------------------------------
    # Get JSON Data
    # ------------------------------------------

    data = request.get_json()


    if not data:

        return jsonify({

            "reply":
            "No message received."

        })


    # ------------------------------------------
    # Get User Message
    # ------------------------------------------

    message = data.get(
        "message",
        ""
    ).strip()


    if message == "":

        return jsonify({

            "reply":
            "Please type a question."

        })


    # ------------------------------------------
    # Chatbot Response
    # ------------------------------------------

    reply = chatbot_service.get_response(
        message
    )


    return jsonify({

        "reply": reply

    })


# ==========================================================
# ADMIN
# ==========================================================

@app.route("/admin")
def admin():

    return render_template(
        "admin.html"
    )


# ==========================================================
# ABOUT
# ==========================================================

@app.route("/about")
def about():

    return render_template(
        "index.html"
    )


# ==========================================================
# CONTACT
# ==========================================================

@app.route("/contact")
def contact():

    return render_template(
        "index.html"
    )


# ==========================================
# 404 Page
# ==========================================

@app.errorhandler(404)
def page_not_found(error):

    return render_template("404.html"), 404


# ==========================================
# Run Flask Application
# ==========================================

if __name__ == "__main__":

    print()
    print("=" * 70)
    print("STARTING HEALTHCARE AI APPLICATION")
    print("=" * 70)
    print("Server: http://127.0.0.1:5000")
    print("Debug mode: OFF")
    print("Auto reloader: OFF")
    print("=" * 70)
    print()

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=False,
        use_reloader=False
    )
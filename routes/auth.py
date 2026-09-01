from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    flash,
    session
)

from werkzeug.security import (
    generate_password_hash,
    check_password_hash
)

from db import get_connection


# ==========================================================
# Authentication Blueprint
# ==========================================================

auth_bp = Blueprint(
    "auth_bp",
    __name__
)


# ==========================================================
# Register
# ==========================================================

@auth_bp.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        full_name = request.form.get("full_name", "").strip()
        email = request.form.get("email", "").strip().lower()
        phone = request.form.get("phone", "").strip()
        password = request.form.get("password", "")
        gender = request.form.get("gender", "").strip()
        age = request.form.get("age", "").strip()

        # ------------------------------------------
        # Basic Validation
        # ------------------------------------------

        if not full_name or not email or not password:

            flash(
                "Please fill all required fields.",
                "danger"
            )

            return render_template(
                "register.html"
            )

        try:

            connection = get_connection()

            if connection is None:

                flash(
                    "Database connection failed.",
                    "danger"
                )

                return render_template(
                    "register.html"
                )

            cursor = connection.cursor()

            # ------------------------------------------
            # Check Existing Email
            # ------------------------------------------

            cursor.execute(
                """
                SELECT user_id
                FROM users
                WHERE LOWER(email) = :1
                """,
                [email]
            )

            existing_user = cursor.fetchone()

            if existing_user:

                flash(
                    "Email already registered.",
                    "warning"
                )

                cursor.close()
                connection.close()

                return render_template(
                    "register.html"
                )

            # ------------------------------------------
            # Hash Password
            # ------------------------------------------

            hashed_password = generate_password_hash(
                password
            )

            # ------------------------------------------
            # Insert User
            # ------------------------------------------

            cursor.execute(
                """
                INSERT INTO users
                (
                    full_name,
                    email,
                    phone,
                    password,
                    gender,
                    age
                )
                VALUES
                (
                    :1,
                    :2,
                    :3,
                    :4,
                    :5,
                    :6
                )
                """,
                [
                    full_name,
                    email,
                    phone,
                    hashed_password,
                    gender,
                    age
                ]
            )

            connection.commit()

            cursor.close()
            connection.close()

            flash(
                "Registration successful. Please login.",
                "success"
            )

            return redirect(
                url_for("auth_bp.login")
            )

        except Exception as e:

            print(
                "REGISTER ERROR:",
                e
            )

            flash(
                "Registration failed. Please try again.",
                "danger"
            )

    return render_template(
        "register.html"
    )


# ==========================================================
# Login
# ==========================================================

@auth_bp.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        email = request.form.get(
            "email",
            ""
        ).strip().lower()

        password = request.form.get(
            "password",
            ""
        )

        try:

            connection = get_connection()

            if connection is None:

                flash(
                    "Database connection failed.",
                    "danger"
                )

                return render_template(
                    "login.html"
                )

            cursor = connection.cursor()

            # ------------------------------------------
            # Get User
            # ------------------------------------------

            cursor.execute(
                """
                SELECT
                    user_id,
                    full_name,
                    email,
                    phone,
                    gender,
                    age,
                    password
                FROM users
                WHERE LOWER(email) = :1
                """,
                [email]
            )

            user = cursor.fetchone()

            cursor.close()
            connection.close()

            # ------------------------------------------
            # User Not Found
            # ------------------------------------------

            if user is None:

                flash(
                    "Invalid Email or Password.",
                    "danger"
                )

                return render_template(
                    "login.html"
                )

            # ------------------------------------------
            # Check Password
            # ------------------------------------------

            password_correct = check_password_hash(
                user[6],
                password
            )

            if password_correct:

                session["user_id"] = user[0]
                session["user_name"] = user[1]
                session["email"] = user[2]
                session["phone"] = user[3]
                session["gender"] = user[4]
                session["age"] = user[5]

                flash(
                    "Login successful.",
                    "success"
                )

                return redirect(
                    url_for("dashboard")
                )

            else:

                flash(
                    "Invalid Email or Password.",
                    "danger"
                )

        except Exception as e:

            print(
                "LOGIN ERROR:",
                e
            )

            flash(
                "Login failed. Please try again.",
                "danger"
            )

    return render_template(
        "login.html"
    )


# ==========================================================
# Logout
# ==========================================================

@auth_bp.route("/logout")
def logout():

    session.clear()

    flash(
        "Logged out successfully.",
        "success"
    )

    return redirect(
        url_for("home")
    )


# ==========================================================
# Forgot Password
# ==========================================================

@auth_bp.route(
    "/forgot-password",
    methods=["GET", "POST"]
)
def forgot_password():

    # ======================================================
    # GET
    # ======================================================

    if request.method == "GET":

        return render_template(
            "forgot_password.html"
        )

    # ======================================================
    # POST
    # ======================================================

    email = request.form.get(
        "email",
        ""
    ).strip().lower()

    new_password = request.form.get(
        "new_password",
        ""
    )

    confirm_password = request.form.get(
        "confirm_password",
        ""
    )

    # ======================================================
    # Validation
    # ======================================================

    if not email:

        flash(
            "Please enter your registered email.",
            "danger"
        )

        return render_template(
            "forgot_password.html"
        )

    if not new_password:

        flash(
            "Please enter a new password.",
            "danger"
        )

        return render_template(
            "forgot_password.html"
        )

    if len(new_password) < 6:

        flash(
            "Password must contain at least 6 characters.",
            "warning"
        )

        return render_template(
            "forgot_password.html"
        )

    if new_password != confirm_password:

        flash(
            "New passwords do not match.",
            "danger"
        )

        return render_template(
            "forgot_password.html"
        )

    # ======================================================
    # Database
    # ======================================================

    connection = None
    cursor = None

    try:

        connection = get_connection()

        if connection is None:

            flash(
                "Database connection failed.",
                "danger"
            )

            return render_template(
                "forgot_password.html"
            )

        cursor = connection.cursor()

        # ==================================================
        # Check Registered Email
        # ==================================================

        cursor.execute(
            """
            SELECT user_id
            FROM users
            WHERE LOWER(email) = :1
            """,
            [email]
        )

        user = cursor.fetchone()

        if user is None:

            flash(
                "No account found with this email address.",
                "danger"
            )

            return render_template(
                "forgot_password.html"
            )

        # ==================================================
        # Hash New Password
        # ==================================================

        hashed_password = generate_password_hash(
            new_password
        )

        # ==================================================
        # Update Password
        # ==================================================

        cursor.execute(
            """
            UPDATE users
            SET password = :1
            WHERE user_id = :2
            """,
            [
                hashed_password,
                user[0]
            ]
        )

        connection.commit()

        flash(
            "Password reset successfully. Please login with your new password.",
            "success"
        )

        return redirect(
            url_for("auth_bp.login")
        )

    except Exception as e:

        if connection:
            connection.rollback()

        print(
            "PASSWORD RESET ERROR:",
            e
        )

        flash(
            "Unable to reset password. Please try again.",
            "danger"
        )

        return render_template(
            "forgot_password.html"
        )

    finally:

        if cursor:

            cursor.close()

        if connection:

            connection.close()
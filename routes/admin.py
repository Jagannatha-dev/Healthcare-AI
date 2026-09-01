import os
import pandas as pd
from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from db import get_connection

admin_bp = Blueprint("admin", __name__, url_prefix="/admin")
DATASET_FOLDER = os.path.join(os.getcwd(), "dataset")


# ---------------------------
# Admin Login
# ---------------------------
@admin_bp.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT ADMIN_ID, USERNAME
            FROM ADMIN
            WHERE USERNAME=:1 AND PASSWORD=:2
        """, (username, password))

        admin = cursor.fetchone()

        cursor.close()
        conn.close()

        if admin:
            session["admin"] = admin[1]
            return redirect(url_for("admin.dashboard"))
        else:
            flash("Invalid Username or Password", "danger")

    return render_template("admin/admin_login.html")

# ---------------------------
# Dashboard
# ---------------------------
@admin_bp.route("/dashboard")
def dashboard():

    if "admin" not in session:
        return redirect(url_for("admin.login"))

    conn = get_connection()
    cursor = conn.cursor()

    # =====================================
    # Total Users
    # =====================================
    cursor.execute("""
        SELECT COUNT(*)
        FROM USERS
    """)
    total_users = cursor.fetchone()[0]

    # =====================================
    # Total Predictions
    # =====================================
    cursor.execute("""
        SELECT COUNT(*)
        FROM PREDICTION_HISTORY
    """)
    total_predictions = cursor.fetchone()[0]

    # =====================================
    # Today's Predictions
    # =====================================
    cursor.execute("""
        SELECT COUNT(*)
        FROM PREDICTION_HISTORY
        WHERE TRUNC(PREDICTION_DATE)=TRUNC(SYSDATE)
    """)
    today_predictions = cursor.fetchone()[0]

    # =====================================
    # Most Predicted Disease
    # =====================================
    cursor.execute("""
        SELECT
            DISEASE_NAME,
            COUNT(*) TOTAL
        FROM PREDICTION_HISTORY
        GROUP BY DISEASE_NAME
        ORDER BY TOTAL DESC
        FETCH FIRST 1 ROWS ONLY
    """)

    disease = cursor.fetchone()

    if disease:
        top_disease = disease[0]
        top_count = disease[1]
    else:
        top_disease = "No Data"
        top_count = 0

    # =====================================
    # Recent Predictions
    # =====================================
    cursor.execute("""
        SELECT
            U.FULL_NAME,
            P.DISEASE_NAME,
            P.CONFIDENCE,
            P.PREDICTION_DATE
        FROM PREDICTION_HISTORY P
        JOIN USERS U
            ON P.USER_ID = U.USER_ID
        ORDER BY P.PREDICTION_DATE DESC
        FETCH FIRST 5 ROWS ONLY
    """)

    recent_predictions = cursor.fetchall()

    # =====================================
    # Disease Analytics
    # =====================================
    cursor.execute("""
        SELECT
            DISEASE_NAME,
            COUNT(*)
        FROM PREDICTION_HISTORY
        GROUP BY DISEASE_NAME
        ORDER BY COUNT(*) DESC
    """)

    disease_rows = cursor.fetchall()

    labels = []
    counts = []

    for row in disease_rows:
        labels.append(row[0])
        counts.append(row[1])

    # =====================================
    # Monthly Prediction Analytics
    # =====================================
    cursor.execute("""
        SELECT
            TO_CHAR(PREDICTION_DATE,'Mon'),
            COUNT(*)
        FROM PREDICTION_HISTORY
        GROUP BY TO_CHAR(PREDICTION_DATE,'Mon'),
                 TO_CHAR(PREDICTION_DATE,'MM')
        ORDER BY TO_CHAR(PREDICTION_DATE,'MM')
    """)

    month_rows = cursor.fetchall()

    month_labels = []
    month_counts = []

    for row in month_rows:
        month_labels.append(row[0])
        month_counts.append(row[1])

    cursor.close()
    conn.close()

    return render_template(
        "admin/dashboard.html",

        total_users=total_users,

        total_predictions=total_predictions,

        today_predictions=today_predictions,

        top_disease=top_disease,

        top_count=top_count,

        recent_predictions=recent_predictions,

        labels=labels,

        counts=counts,

        month_labels=month_labels,

        month_counts=month_counts
    )
# ==========================
# View All Users
# ==========================

@admin_bp.route("/users")
def users():

    if "admin" not in session:
        return redirect(url_for("admin.login"))

    search = request.args.get("search", "")

    conn = get_connection()
    cursor = conn.cursor()

    if search:

        cursor.execute("""
        SELECT USER_ID,
               FULL_NAME,
               EMAIL,
               PHONE,
               AGE,
               GENDER
        FROM USERS
        WHERE
        LOWER(FULL_NAME) LIKE :1
        OR
        LOWER(EMAIL) LIKE :2
        ORDER BY USER_ID
        """,

        ("%"+search.lower()+"%",
         "%"+search.lower()+"%"))

    else:

        cursor.execute("""
        SELECT USER_ID,
               FULL_NAME,
               EMAIL,
               PHONE,
               AGE,
               GENDER
        FROM USERS
        ORDER BY USER_ID
        """)

    users = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template(
        "admin/users.html",
        users=users
    )

# ==========================
# View User
# ==========================

@admin_bp.route("/view-user/<int:user_id>")
def view_user(user_id):

    if "admin" not in session:
        return redirect(url_for("admin.login"))

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT USER_ID,
               FULL_NAME,
               EMAIL,
               PHONE,
               AGE,
               GENDER
        FROM USERS
        WHERE USER_ID = :1
    """, (user_id,))

    user = cursor.fetchone()

    cursor.close()
    conn.close()

    if user is None:
        flash("User not found.", "danger")
        return redirect(url_for("admin.users"))

    return render_template(
        "admin/view_user.html",
        user=user
    )

# ==========================
# Edit User
# ==========================

@admin_bp.route("/edit-user/<int:user_id>", methods=["GET", "POST"])
def edit_user(user_id):

    if "admin" not in session:
        return redirect(url_for("admin.login"))

    conn = get_connection()
    cursor = conn.cursor()

    if request.method == "POST":

        full_name = request.form["full_name"]
        email = request.form["email"]
        phone = request.form["phone"]
        gender = request.form["gender"]
        age = request.form["age"]

        cursor.execute("""
            UPDATE USERS
            SET FULL_NAME = :1,
                EMAIL = :2,
                PHONE = :3,
                GENDER = :4,
                AGE = :5
            WHERE USER_ID = :6
        """, (full_name, email, phone, gender, age, user_id))

        conn.commit()

        cursor.close()
        conn.close()

        flash("User updated successfully!", "success")

        return redirect(url_for("admin.users"))

    cursor.execute("""
        SELECT USER_ID,
               FULL_NAME,
               EMAIL,
               PHONE,
               GENDER,
               AGE
        FROM USERS
        WHERE USER_ID = :1
    """, (user_id,))

    user = cursor.fetchone()

    cursor.close()
    conn.close()

    return render_template(
        "admin/edit_user.html",
        user=user
    )

# ==========================
# Prediction Management
# ==========================

@admin_bp.route("/predictions")
def predictions():

    if "admin" not in session:
        return redirect(url_for("admin.login"))

    search = request.args.get("search", "")

    conn = get_connection()
    cursor = conn.cursor()

    if search:

        cursor.execute("""
            SELECT
                P.HISTORY_ID,
                U.FULL_NAME,
                P.DISEASE_NAME,
                P.CONFIDENCE,
                P.PREDICTION_DATE
            FROM PREDICTION_HISTORY P
            JOIN USERS U
              ON P.USER_ID = U.USER_ID
            WHERE
                LOWER(U.FULL_NAME) LIKE :1
                OR LOWER(P.DISEASE_NAME) LIKE :2
            ORDER BY P.PREDICTION_DATE DESC
        """,
        ("%"+search.lower()+"%",
         "%"+search.lower()+"%"))

    else:

        cursor.execute("""
            SELECT
                P.HISTORY_ID,
                U.FULL_NAME,
                P.DISEASE_NAME,
                P.CONFIDENCE,
                P.PREDICTION_DATE
            FROM PREDICTION_HISTORY P
            JOIN USERS U
              ON P.USER_ID = U.USER_ID
            ORDER BY P.PREDICTION_DATE DESC
        """)

    predictions = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template(
        "admin/predictions.html",
        predictions=predictions
    )

# ==========================
# View Prediction
# ==========================

@admin_bp.route("/view-prediction/<int:history_id>")
def view_prediction(history_id):

    if "admin" not in session:
        return redirect(url_for("admin.login"))

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            P.HISTORY_ID,
            U.FULL_NAME,
            U.EMAIL,
            P.DISEASE_NAME,
            P.CONFIDENCE,
            P.SYMPTOMS,
            P.PREDICTION_DATE
        FROM PREDICTION_HISTORY P
        JOIN USERS U
        ON P.USER_ID = U.USER_ID
        WHERE P.HISTORY_ID = :1
    """, (history_id,))

    prediction = cursor.fetchone()

    if prediction:

        prediction = list(prediction)

        if prediction[5]:
            prediction[5] = prediction[5].read()

    cursor.close()
    conn.close()

    if prediction is None:
        flash("Prediction not found.", "danger")
        return redirect(url_for("admin.predictions"))

    return render_template(
        "admin/view_prediction.html",
        prediction=prediction
    )


# ==========================
# Delete Prediction
# ==========================

@admin_bp.route("/delete-prediction/<int:history_id>")
def delete_prediction(history_id):

    if "admin" not in session:
        return redirect(url_for("admin.login"))

    conn = get_connection()
    cursor = conn.cursor()

    try:

        cursor.execute(
            "DELETE FROM PREDICTION_HISTORY WHERE HISTORY_ID = :1",
            (history_id,)
        )

        conn.commit()

        flash("Prediction deleted successfully!", "success")

    except Exception as e:

        conn.rollback()
        flash(str(e), "danger")

    finally:

        cursor.close()
        conn.close()

    return redirect(url_for("admin.predictions"))
# ==========================
# Delete User
# ==========================

@admin_bp.route("/delete-user/<int:user_id>")
def delete_user(user_id):

    if "admin" not in session:
        return redirect(url_for("admin.login"))

    conn = get_connection()
    cursor = conn.cursor()

    try:
        # Delete prediction history first
        cursor.execute(
            "DELETE FROM PREDICTION_HISTORY WHERE USER_ID = :1",
            (user_id,)
        )

        # Delete user
        cursor.execute(
            "DELETE FROM USERS WHERE USER_ID = :1",
            (user_id,)
        )

        conn.commit()

        flash("User deleted successfully!", "success")

    except Exception as e:
        conn.rollback()
        flash(str(e), "danger")

    finally:
        cursor.close()
        conn.close()

    return redirect(url_for("admin.users"))

# -----------------------------
# Diseases
# -----------------------------
from pandas.errors import EmptyDataError

@admin_bp.route("/datasets")
def datasets():

    if "admin" not in session:
        return redirect(url_for("admin.login"))

    csv_files = []

    for file in os.listdir(DATASET_FOLDER):

        if file.endswith(".csv"):

            path = os.path.join(DATASET_FOLDER, file)

            try:
                print("Reading:", file)

                df = pd.read_csv(path)

                csv_files.append({
                    "name": file,
                    "rows": len(df),
                    "columns": len(df.columns)
                })

            except EmptyDataError:
                print(f"{file} is empty.")

                csv_files.append({
                    "name": file,
                    "rows": 0,
                    "columns": 0
                })

            except Exception as e:
                print(f"Error reading {file}: {e}")

    return render_template(
        "admin/datasets.html",
        csv_files=csv_files
    )
@admin_bp.route("/datasets/<filename>")
def view_dataset(filename):

    if "admin" not in session:
        return redirect(url_for("admin.login"))

    path = os.path.join(DATASET_FOLDER, filename)

    df = pd.read_csv(path)

    data = df.to_dict(orient="records")
    columns = df.columns.tolist()

    return render_template(
        "admin/view_dataset.html",
        filename=filename,
        columns=columns,
        data=data
    )

# ==========================
# Edit Dataset Row
# ==========================

@admin_bp.route(
    "/datasets/<path:filename>/edit/<int:row_index>",
    methods=["GET", "POST"]
)
def edit_dataset_row(filename, row_index):

    # ------------------------------------------
    # Admin Login Check
    # ------------------------------------------

    if "admin" not in session:
        return redirect(url_for("admin.login"))

    # ------------------------------------------
    # Dataset Path
    # ------------------------------------------

    path = os.path.join(
        DATASET_FOLDER,
        filename
    )

    # ------------------------------------------
    # Check File Exists
    # ------------------------------------------

    if not os.path.isfile(path):

        flash(
            "Dataset file not found.",
            "danger"
        )

        return redirect(
            url_for("admin.datasets")
        )

    # ------------------------------------------
    # Read CSV
    # ------------------------------------------

    try:

        df = pd.read_csv(path)

    except EmptyDataError:

        flash(
            "This dataset is empty.",
            "warning"
        )

        return redirect(
            url_for("admin.datasets")
        )

    except Exception as e:

        flash(
            f"Unable to read dataset: {e}",
            "danger"
        )

        return redirect(
            url_for("admin.datasets")
        )

    # ------------------------------------------
    # Check Row Index
    # ------------------------------------------

    if row_index < 0 or row_index >= len(df):

        flash(
            "Invalid dataset row.",
            "danger"
        )

        return redirect(
            url_for(
                "admin.view_dataset",
                filename=filename
            )
        )

    # ------------------------------------------
    # POST - Save Changes
    # ------------------------------------------

    if request.method == "POST":

        try:

            # Update each column
            for column in df.columns:

                value = request.form.get(
                    column,
                    ""
                )

                df.at[row_index, column] = value

            # ----------------------------------
            # Save CSV
            # ----------------------------------

            df.to_csv(
                path,
                index=False
            )

            flash(
                "Dataset row updated successfully!",
                "success"
            )

            # IMPORTANT:
            # Always return after successful POST

            return redirect(
                url_for(
                    "admin.view_dataset",
                    filename=filename
                )
            )

        except Exception as e:

            flash(
                f"Unable to save changes: {e}",
                "danger"
            )

            # IMPORTANT:
            # Return a response even when saving fails

            row = df.iloc[row_index].to_dict()

            return render_template(
                "admin/edit_dataset_row.html",
                filename=filename,
                row=row,
                columns=df.columns.tolist(),
                row_index=row_index
            )

    # ------------------------------------------
    # GET - Display Edit Form
    # ------------------------------------------

    row = df.iloc[row_index].to_dict()

    columns = df.columns.tolist()

    return render_template(
        "admin/edit_dataset_row.html",
        filename=filename,
        row=row,
        columns=columns,
        row_index=row_index
    )

# ==========================
# Add Dataset Row
# ==========================

@admin_bp.route(
    "/datasets/<path:filename>/add",
    methods=["GET", "POST"]
)
def add_dataset_row(filename):

    # ------------------------------------------
    # Admin Login Check
    # ------------------------------------------

    if "admin" not in session:
        return redirect(url_for("admin.login"))

    # ------------------------------------------
    # Dataset Path
    # ------------------------------------------

    path = os.path.join(
        DATASET_FOLDER,
        filename
    )

    # ------------------------------------------
    # Check File
    # ------------------------------------------

    if not os.path.isfile(path):

        flash(
            "Dataset file not found.",
            "danger"
        )

        return redirect(
            url_for("admin.datasets")
        )

    # ------------------------------------------
    # Read CSV
    # ------------------------------------------

    try:

        df = pd.read_csv(path)

    except EmptyDataError:

        flash(
            "This dataset is empty or has no columns.",
            "warning"
        )

        return redirect(
            url_for("admin.datasets")
        )

    except Exception as e:

        flash(
            f"Unable to read dataset: {e}",
            "danger"
        )

        return redirect(
            url_for("admin.datasets")
        )

    # ------------------------------------------
    # Get Columns
    # ------------------------------------------

    columns = df.columns.tolist()

    # ------------------------------------------
    # POST - Add New Row
    # ------------------------------------------

    if request.method == "POST":

        try:

            new_row = {}

            for column in columns:

                new_row[column] = request.form.get(
                    column,
                    ""
                )

            # Add new row
            df.loc[len(df)] = new_row

            # Save CSV
            df.to_csv(
                path,
                index=False
            )

            flash(
                "New dataset row added successfully!",
                "success"
            )

            return redirect(
                url_for(
                    "admin.view_dataset",
                    filename=filename
                )
            )

        except Exception as e:

            flash(
                f"Unable to add row: {e}",
                "danger"
            )

            return render_template(
                "admin/add_dataset_row.html",
                filename=filename,
                columns=columns
            )

    # ------------------------------------------
    # GET - Show Add Row Form
    # ------------------------------------------

    return render_template(
        "admin/add_dataset_row.html",
        filename=filename,
        columns=columns
    )
# ==========================
# Delete Dataset Row
# ==========================

@admin_bp.route(
    "/datasets/<path:filename>/delete/<int:row_index>",
    methods=["GET"]
)
def delete_dataset_row(filename, row_index):

    # ------------------------------------------
    # Admin Login Check
    # ------------------------------------------

    if "admin" not in session:
        return redirect(url_for("admin.login"))

    # ------------------------------------------
    # Dataset Path
    # ------------------------------------------

    path = os.path.join(
        DATASET_FOLDER,
        filename
    )

    # ------------------------------------------
    # Check File
    # ------------------------------------------

    if not os.path.isfile(path):

        flash(
            "Dataset file not found.",
            "danger"
        )

        return redirect(
            url_for("admin.datasets")
        )

    # ------------------------------------------
    # Read CSV
    # ------------------------------------------

    try:

        df = pd.read_csv(path)

    except EmptyDataError:

        flash(
            "Dataset is empty.",
            "warning"
        )

        return redirect(
            url_for(
                "admin.view_dataset",
                filename=filename
            )
        )

    except Exception as e:

        flash(
            f"Unable to read dataset: {e}",
            "danger"
        )

        return redirect(
            url_for("admin.datasets")
        )

    # ------------------------------------------
    # Check Row Index
    # ------------------------------------------

    if row_index < 0 or row_index >= len(df):

        flash(
            "Invalid dataset row.",
            "danger"
        )

        return redirect(
            url_for(
                "admin.view_dataset",
                filename=filename
            )
        )

    # ------------------------------------------
    # Delete Row
    # ------------------------------------------

    try:

        # Remove selected row
        df = df.drop(
            df.index[row_index]
        )

        # Reset row indexes
        df = df.reset_index(
            drop=True
        )

        # Save updated CSV
        df.to_csv(
            path,
            index=False
        )

        flash(
            "Dataset row deleted successfully!",
            "success"
        )

    except Exception as e:

        flash(
            f"Unable to delete row: {e}",
            "danger"
        )

    # ------------------------------------------
    # Return to Dataset
    # ------------------------------------------

    return redirect(
        url_for(
            "admin.view_dataset",
            filename=filename
        )
    )
# ==========================
# Analytics
# ==========================

@admin_bp.route("/analytics")
def analytics():

    if "admin" not in session:
        return redirect(url_for("admin.login"))

    conn = get_connection()
    cursor = conn.cursor()

    try:

        # ----------------------------------
        # Total Users
        # ----------------------------------

        cursor.execute("""
            SELECT COUNT(*)
            FROM USERS
        """)

        total_users = cursor.fetchone()[0]


        # ----------------------------------
        # Total Predictions
        # ----------------------------------

        cursor.execute("""
            SELECT COUNT(*)
            FROM PREDICTION_HISTORY
        """)

        total_predictions = cursor.fetchone()[0]


        # ----------------------------------
        # Most Predicted Disease
        # ----------------------------------

        cursor.execute("""
            SELECT DISEASE_NAME, COUNT(*) AS TOTAL
            FROM PREDICTION_HISTORY
            GROUP BY DISEASE_NAME
            ORDER BY TOTAL DESC
            FETCH FIRST 1 ROW ONLY
        """)

        most_predicted = cursor.fetchone()

        if most_predicted:

            most_predicted_disease = most_predicted[0]
            most_predicted_count = most_predicted[1]

        else:

            most_predicted_disease = "No Data"
            most_predicted_count = 0


        # ----------------------------------
        # Disease Statistics
        # ----------------------------------

        cursor.execute("""
            SELECT
                DISEASE_NAME,
                COUNT(*) AS TOTAL
            FROM PREDICTION_HISTORY
            GROUP BY DISEASE_NAME
            ORDER BY TOTAL DESC
        """)

        disease_stats = cursor.fetchall()


        # ----------------------------------
        # Daily Prediction Statistics
        # ----------------------------------

        cursor.execute("""
            SELECT
                TRUNC(PREDICTION_DATE),
                COUNT(*)
            FROM PREDICTION_HISTORY
            GROUP BY TRUNC(PREDICTION_DATE)
            ORDER BY TRUNC(PREDICTION_DATE)
        """)

        daily_stats = cursor.fetchall()

        return render_template(
            "admin/analytics.html",
            total_users=total_users,
            total_predictions=total_predictions,
            most_predicted_disease=most_predicted_disease,
            most_predicted_count=most_predicted_count,
            disease_stats=disease_stats,
            daily_stats=daily_stats
        )

    finally:

        cursor.close()
        conn.close()
# ---------------------------
# Logout
# ---------------------------
@admin_bp.route("/logout")
def logout():
    session.pop("admin", None)
    return redirect(url_for("admin.login"))

import os
import pandas as pd
from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from db import get_connection
from pandas.errors import EmptyDataError

admin_bp = Blueprint("admin", __name__, url_prefix="/admin")
DATASET_FOLDER = os.path.abspath(os.path.join(os.path.dirname(os.path.dirname(__file__)), "dataset"))


def _connection_or_error():
    conn = get_connection()
    if conn is None:
        flash("Database connection is unavailable. Please try again.", "danger")
    return conn


def _safe_close(cursor=None, conn=None):
    if cursor is not None:
        try:
            cursor.close()
        except Exception:
            pass
    if conn is not None:
        try:
            conn.close()
        except Exception:
            pass


@admin_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")

        if not username or not password:
            flash("Username and Password are required.", "danger")
            return render_template("admin/admin_login.html")

        conn = _connection_or_error()
        if conn is None:
            return render_template("admin/admin_login.html")

        cursor = None
        try:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT ADMIN_ID, USERNAME
                FROM ADMIN
                WHERE USERNAME=:1 AND PASSWORD=:2
            """, (username, password))
            admin = cursor.fetchone()
            if admin:
                session["admin"] = admin[1]
                return redirect(url_for("admin.dashboard"))
            flash("Invalid Username or Password", "danger")
        except Exception as e:
            print("Admin login database error:", e)
            flash("Unable to access the database. Please try again.", "danger")
        finally:
            _safe_close(cursor, conn)

    return render_template("admin/admin_login.html")


@admin_bp.route("/dashboard")
def dashboard():
    if "admin" not in session:
        return redirect(url_for("admin.login"))

    conn = _connection_or_error()
    if conn is None:
        return redirect(url_for("admin.login"))

    cursor = None
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM USERS")
        total_users = cursor.fetchone()[0]
        cursor.execute("SELECT COUNT(*) FROM PREDICTION_HISTORY")
        total_predictions = cursor.fetchone()[0]
        cursor.execute("""
            SELECT COUNT(*) FROM PREDICTION_HISTORY
            WHERE TRUNC(PREDICTION_DATE)=TRUNC(SYSDATE)
        """)
        today_predictions = cursor.fetchone()[0]

        cursor.execute("""
            SELECT DISEASE_NAME, COUNT(*) TOTAL
            FROM PREDICTION_HISTORY
            GROUP BY DISEASE_NAME
            ORDER BY TOTAL DESC
            FETCH FIRST 1 ROWS ONLY
        """)
        disease = cursor.fetchone()
        top_disease, top_count = (disease[0], disease[1]) if disease else ("No Data", 0)

        cursor.execute("""
            SELECT U.FULL_NAME, P.DISEASE_NAME, P.CONFIDENCE, P.PREDICTION_DATE
            FROM PREDICTION_HISTORY P
            JOIN USERS U ON P.USER_ID = U.USER_ID
            ORDER BY P.PREDICTION_DATE DESC
            FETCH FIRST 5 ROWS ONLY
        """)
        recent_predictions = cursor.fetchall()

        cursor.execute("""
            SELECT DISEASE_NAME, COUNT(*)
            FROM PREDICTION_HISTORY
            GROUP BY DISEASE_NAME
            ORDER BY COUNT(*) DESC
        """)
        disease_rows = cursor.fetchall()
        labels = [row[0] for row in disease_rows]
        counts = [row[1] for row in disease_rows]

        cursor.execute("""
            SELECT TO_CHAR(PREDICTION_DATE,'Mon'), COUNT(*)
            FROM PREDICTION_HISTORY
            GROUP BY TO_CHAR(PREDICTION_DATE,'Mon'), TO_CHAR(PREDICTION_DATE,'MM')
            ORDER BY TO_CHAR(PREDICTION_DATE,'MM')
        """)
        month_rows = cursor.fetchall()
        month_labels = [row[0] for row in month_rows]
        month_counts = [row[1] for row in month_rows]

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
    except Exception as e:
        print("Admin dashboard database error:", e)
        flash("Unable to load dashboard data. Please try again.", "danger")
        return redirect(url_for("admin.login"))
    finally:
        _safe_close(cursor, conn)


@admin_bp.route("/users")
def users():
    if "admin" not in session:
        return redirect(url_for("admin.login"))

    search = request.args.get("search", "").strip()
    conn = _connection_or_error()
    if conn is None:
        return redirect(url_for("admin.dashboard"))

    cursor = None
    try:
        cursor = conn.cursor()
        if search:
            value = f"%{search.lower()}%"
            cursor.execute("""
                SELECT USER_ID, FULL_NAME, EMAIL, PHONE, AGE, GENDER
                FROM USERS
                WHERE LOWER(FULL_NAME) LIKE :1 OR LOWER(EMAIL) LIKE :2
                ORDER BY USER_ID
            """, (value, value))
        else:
            cursor.execute("""
                SELECT USER_ID, FULL_NAME, EMAIL, PHONE, AGE, GENDER
                FROM USERS
                ORDER BY USER_ID
            """)
        return render_template("admin/users.html", users=cursor.fetchall())
    except Exception as e:
        print("Admin users database error:", e)
        flash("Unable to load users. Please try again.", "danger")
        return redirect(url_for("admin.dashboard"))
    finally:
        _safe_close(cursor, conn)


@admin_bp.route("/view-user/<int:user_id>")
def view_user(user_id):
    if "admin" not in session:
        return redirect(url_for("admin.login"))

    conn = _connection_or_error()
    if conn is None:
        return redirect(url_for("admin.users"))

    cursor = None
    try:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT USER_ID, FULL_NAME, EMAIL, PHONE, AGE, GENDER
            FROM USERS WHERE USER_ID=:1
        """, (user_id,))
        user = cursor.fetchone()
        if user is None:
            flash("User not found.", "danger")
            return redirect(url_for("admin.users"))
        return render_template("admin/view_user.html", user=user)
    except Exception as e:
        print("Admin view user database error:", e)
        flash("Unable to load user details. Please try again.", "danger")
        return redirect(url_for("admin.users"))
    finally:
        _safe_close(cursor, conn)


@admin_bp.route("/edit-user/<int:user_id>", methods=["GET", "POST"])
def edit_user(user_id):
    if "admin" not in session:
        return redirect(url_for("admin.login"))

    conn = _connection_or_error()
    if conn is None:
        return redirect(url_for("admin.users"))

    cursor = None
    try:
        cursor = conn.cursor()
        if request.method == "POST":
            full_name = request.form.get("full_name", "").strip()
            email = request.form.get("email", "").strip()
            phone = request.form.get("phone", "").strip()
            gender = request.form.get("gender", "").strip()
            age = request.form.get("age", "").strip()
            cursor.execute("""
                UPDATE USERS
                SET FULL_NAME=:1, EMAIL=:2, PHONE=:3, GENDER=:4, AGE=:5
                WHERE USER_ID=:6
            """, (full_name, email, phone, gender, age, user_id))
            conn.commit()
            flash("User updated successfully!", "success")
            return redirect(url_for("admin.users"))

        cursor.execute("""
            SELECT USER_ID, FULL_NAME, EMAIL, PHONE, GENDER, AGE
            FROM USERS WHERE USER_ID=:1
        """, (user_id,))
        user = cursor.fetchone()
        if user is None:
            flash("User not found.", "danger")
            return redirect(url_for("admin.users"))
        return render_template("admin/edit_user.html", user=user)
    except Exception as e:
        try:
            conn.rollback()
        except Exception:
            pass
        print("Admin edit user database error:", e)
        flash("Unable to update user. Please check the details and try again.", "danger")
        return redirect(url_for("admin.users"))
    finally:
        _safe_close(cursor, conn)


@admin_bp.route("/predictions")
def predictions():
    if "admin" not in session:
        return redirect(url_for("admin.login"))

    search = request.args.get("search", "").strip()
    conn = _connection_or_error()
    if conn is None:
        return redirect(url_for("admin.dashboard"))

    cursor = None
    try:
        cursor = conn.cursor()
        if search:
            value = f"%{search.lower()}%"
            cursor.execute("""
                SELECT P.HISTORY_ID, U.FULL_NAME, P.DISEASE_NAME,
                       P.CONFIDENCE, P.PREDICTION_DATE
                FROM PREDICTION_HISTORY P
                JOIN USERS U ON P.USER_ID=U.USER_ID
                WHERE LOWER(U.FULL_NAME) LIKE :1 OR LOWER(P.DISEASE_NAME) LIKE :2
                ORDER BY P.PREDICTION_DATE DESC
            """, (value, value))
        else:
            cursor.execute("""
                SELECT P.HISTORY_ID, U.FULL_NAME, P.DISEASE_NAME,
                       P.CONFIDENCE, P.PREDICTION_DATE
                FROM PREDICTION_HISTORY P
                JOIN USERS U ON P.USER_ID=U.USER_ID
                ORDER BY P.PREDICTION_DATE DESC
            """)
        return render_template("admin/predictions.html", predictions=cursor.fetchall())
    except Exception as e:
        print("Admin predictions database error:", e)
        flash("Unable to load predictions. Please try again.", "danger")
        return redirect(url_for("admin.dashboard"))
    finally:
        _safe_close(cursor, conn)


@admin_bp.route("/view-prediction/<int:history_id>")
def view_prediction(history_id):
    if "admin" not in session:
        return redirect(url_for("admin.login"))

    conn = _connection_or_error()
    if conn is None:
        return redirect(url_for("admin.predictions"))

    cursor = None
    try:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT P.HISTORY_ID, U.FULL_NAME, U.EMAIL, P.DISEASE_NAME,
                   P.CONFIDENCE, P.SYMPTOMS, P.PREDICTION_DATE
            FROM PREDICTION_HISTORY P
            JOIN USERS U ON P.USER_ID=U.USER_ID
            WHERE P.HISTORY_ID=:1
        """, (history_id,))
        prediction = cursor.fetchone()
        if prediction:
            prediction = list(prediction)
            if prediction[5]:
                try:
                    prediction[5] = prediction[5].read()
                except AttributeError:
                    prediction[5] = str(prediction[5])
        if prediction is None:
            flash("Prediction not found.", "danger")
            return redirect(url_for("admin.predictions"))
        return render_template("admin/view_prediction.html", prediction=prediction)
    except Exception as e:
        print("Admin view prediction database error:", e)
        flash("Unable to load prediction details. Please try again.", "danger")
        return redirect(url_for("admin.predictions"))
    finally:
        _safe_close(cursor, conn)


@admin_bp.route("/delete-prediction/<int:history_id>")
def delete_prediction(history_id):
    if "admin" not in session:
        return redirect(url_for("admin.login"))

    conn = _connection_or_error()
    if conn is None:
        return redirect(url_for("admin.predictions"))

    cursor = None
    try:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM PREDICTION_HISTORY WHERE HISTORY_ID=:1", (history_id,))
        conn.commit()
        flash("Prediction deleted successfully!", "success")
    except Exception as e:
        try:
            conn.rollback()
        except Exception:
            pass
        print("Admin delete prediction database error:", e)
        flash("Unable to delete prediction. Please try again.", "danger")
    finally:
        _safe_close(cursor, conn)
    return redirect(url_for("admin.predictions"))


@admin_bp.route("/delete-user/<int:user_id>")
def delete_user(user_id):
    if "admin" not in session:
        return redirect(url_for("admin.login"))

    conn = _connection_or_error()
    if conn is None:
        return redirect(url_for("admin.users"))

    cursor = None
    try:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM PREDICTION_HISTORY WHERE USER_ID=:1", (user_id,))
        cursor.execute("DELETE FROM USERS WHERE USER_ID=:1", (user_id,))
        conn.commit()
        flash("User deleted successfully!", "success")
    except Exception as e:
        try:
            conn.rollback()
        except Exception:
            pass
        print("Admin delete user database error:", e)
        flash("Unable to delete user. Please try again.", "danger")
    finally:
        _safe_close(cursor, conn)
    return redirect(url_for("admin.users"))


@admin_bp.route("/datasets")
def datasets():
    if "admin" not in session:
        return redirect(url_for("admin.login"))

    csv_files = []
    if not os.path.isdir(DATASET_FOLDER):
        flash("Dataset folder not found.", "danger")
        return render_template("admin/datasets.html", csv_files=csv_files)

    for file in sorted(os.listdir(DATASET_FOLDER)):
        if not file.lower().endswith(".csv"):
            continue
        path = os.path.join(DATASET_FOLDER, file)
        try:
            df = pd.read_csv(path)
            csv_files.append({"name": file, "rows": len(df), "columns": len(df.columns)})
        except EmptyDataError:
            csv_files.append({"name": file, "rows": 0, "columns": 0})
        except Exception as e:
            print(f"Error reading {file}: {e}")
            csv_files.append({"name": file, "rows": 0, "columns": 0})

    return render_template("admin/datasets.html", csv_files=csv_files)


@admin_bp.route("/datasets/<filename>")
def view_dataset(filename):
    if "admin" not in session:
        return redirect(url_for("admin.login"))

    if not filename.lower().endswith(".csv") or os.path.basename(filename) != filename:
        flash("Invalid dataset file.", "danger")
        return redirect(url_for("admin.datasets"))

    path = os.path.join(DATASET_FOLDER, filename)
    if not os.path.isfile(path):
        flash("Dataset file not found.", "danger")
        return redirect(url_for("admin.datasets"))

    try:
        df = pd.read_csv(path)
        return render_template(
            "admin/view_dataset.html",
            filename=filename,
            columns=list(df.columns),
            rows=df.head(100).values.tolist()
        )
    except EmptyDataError:
        return render_template(
            "admin/view_dataset.html",
            filename=filename,
            columns=[],
            rows=[]
        )
    except Exception as e:
        print(f"Error reading {filename}: {e}")
        flash("Unable to read dataset file.", "danger")
        return redirect(url_for("admin.datasets"))


@admin_bp.route("/logout")
def logout():
    session.pop("admin", None)
    return redirect(url_for("admin.login"))

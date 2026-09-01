from werkzeug.security import check_password_hash, generate_password_hash
from db import get_connection


class ProfileService:

    # ==========================================
    # Get Profile
    # ==========================================

    @staticmethod
    def get_profile(user_id):

        conn = get_connection()

        if conn is None:
            return None

        cursor = conn.cursor()

        cursor.execute("""
            SELECT
                full_name,
                email,
                phone,
                gender,
                age,
                created_at
            FROM users
            WHERE user_id = :1
        """, (user_id,))

        row = cursor.fetchone()

        cursor.close()
        conn.close()

        return row

    # ==========================================
    # Total Predictions
    # ==========================================

    @staticmethod
    def get_total_predictions(user_id):

        conn = get_connection()

        if conn is None:
            return 0

        cursor = conn.cursor()

        cursor.execute("""
            SELECT COUNT(*)
            FROM prediction_history
            WHERE user_id = :1
        """, (user_id,))

        total = cursor.fetchone()[0]

        cursor.close()
        conn.close()

        return total

    # ==========================================
    # Update Profile
    # ==========================================

    @staticmethod
    def update_profile(user_id, full_name, phone, gender, age):

        conn = get_connection()

        if conn is None:
            return False

        cursor = conn.cursor()

        cursor.execute("""
            UPDATE users
            SET
                full_name = :1,
                phone = :2,
                gender = :3,
                age = :4
            WHERE user_id = :5
        """, (
            full_name,
            phone,
            gender,
            age,
            user_id
        ))

        conn.commit()

        cursor.close()
        conn.close()

        return True
    
        # ==========================================
    # Change Password
    # ==========================================

    @staticmethod
    def change_password(user_id, current_password, new_password):

        conn = get_connection()

        if conn is None:
            return False, "Database connection failed."

        cursor = conn.cursor()

        cursor.execute("""
        SELECT password
        FROM users
        WHERE user_id = :1
        """, (user_id,))

        row = cursor.fetchone()

        if row is None:

            cursor.close()
            conn.close()

            return False, "User not found."

        db_password = row[0]

    # Verify current password
        if not check_password_hash(db_password, current_password):

            cursor.close()
            conn.close()

            return False, "Current password is incorrect."

    # Hash the new password
        hashed_password = generate_password_hash(new_password)

        cursor.execute("""
        UPDATE users
        SET password = :1
        WHERE user_id = :2
        """, (
        hashed_password,
        user_id
    ))

        conn.commit()

        cursor.close()
        conn.close()

        return True, "Password updated successfully."
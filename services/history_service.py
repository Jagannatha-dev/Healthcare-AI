# ==========================================================
# Healthcare AI - Prediction History Service
# ==========================================================

from db import get_connection


class HistoryService:

    # =========================================================
    # SAVE PREDICTION
    # =========================================================

    @staticmethod
    def save_prediction(
        user_id,
        disease_name,
        confidence,
        symptoms
    ):

        conn = get_connection()

        if conn is None:

            print(
                "[ERROR] Database connection failed."
            )

            return False

        cursor = None

        try:

            cursor = conn.cursor()

            # -------------------------------------------------
            # Convert symptoms to text
            # -------------------------------------------------

            if isinstance(symptoms, (list, tuple)):

                symptoms_text = ",".join(
                    str(symptom).strip()
                    for symptom in symptoms
                    if str(symptom).strip()
                )

            else:

                symptoms_text = str(
                    symptoms
                    if symptoms is not None
                    else ""
                )

            # -------------------------------------------------
            # Insert prediction
            # -------------------------------------------------

            cursor.execute(
                """
                INSERT INTO prediction_history
                (
                    user_id,
                    disease_name,
                    confidence,
                    symptoms
                )
                VALUES
                (
                    :1,
                    :2,
                    :3,
                    :4
                )
                """,
                (
                    user_id,
                    disease_name,
                    confidence,
                    symptoms_text
                )
            )

            conn.commit()

            print(
                f"[HISTORY] Prediction saved: "
                f"{disease_name} | User ID: {user_id}"
            )

            return True

        except Exception as e:

            try:
                conn.rollback()
            except Exception:
                pass

            print(
                "[ERROR] Could not save prediction:"
            )

            print(e)

            return False

        finally:

            if cursor:

                try:
                    cursor.close()
                except Exception:
                    pass

            if conn:

                try:
                    conn.close()
                except Exception:
                    pass


    # =========================================================
    # GET COMPLETE PREDICTION HISTORY
    # =========================================================

    @staticmethod
    def get_history(user_id):

        conn = get_connection()

        if conn is None:

            print(
                "[ERROR] Database connection failed."
            )

            return []

        cursor = None

        try:

            cursor = conn.cursor()

            cursor.execute(
                """
                SELECT
                    history_id,
                    disease_name,
                    confidence,
                    symptoms,
                    prediction_date
                FROM prediction_history
                WHERE user_id = :1
                ORDER BY prediction_date DESC
                """,
                (user_id,)
            )

            rows = []

            for row in cursor.fetchall():

                # ---------------------------------------------
                # Read symptoms CLOB
                # ---------------------------------------------

                symptoms_value = ""

                if row[3] is not None:

                    try:

                        symptoms_value = row[3].read()

                    except AttributeError:

                        symptoms_value = str(
                            row[3]
                        )

                # ---------------------------------------------
                # Store row
                # ---------------------------------------------

                rows.append(
                    (
                        row[0],                 # History ID
                        row[1],                 # Disease
                        row[2],                 # Confidence
                        symptoms_value,         # Symptoms
                        row[4]                  # Prediction Date
                    )
                )

            return rows

        except Exception as e:

            print(
                "[ERROR] Could not get prediction history:"
            )

            print(e)

            return []

        finally:

            if cursor:

                try:
                    cursor.close()
                except Exception:
                    pass

            if conn:

                try:
                    conn.close()
                except Exception:
                    pass


    # =========================================================
    # GET LATEST PREDICTION FOR LOGGED-IN USER
    # =========================================================

    @staticmethod
    def get_latest_prediction(user_id):

        history = HistoryService.get_history(
            user_id
        )

        if not history:

            print(
                f"[HISTORY] No predictions found "
                f"for user ID: {user_id}"
            )

            return {
                "history_id": None,
                "disease": None,
                "confidence": None,
                "symptoms": "",
                "date": None
            }

        # -----------------------------------------------------
        # First record is latest because get_history()
        # sorts prediction_date DESC
        # -----------------------------------------------------

        latest = history[0]

        latest_prediction = {

            "history_id":
                latest[0],

            "disease":
                latest[1],

            "confidence":
                (
                    float(latest[2])
                    if latest[2] is not None
                    else None
                ),

            "symptoms":
                latest[3],

            "date":
                latest[4]
        }

        print("=" * 60)
        print("LATEST PREDICTION")
        print("=" * 60)

        print(
            f"User ID   : {user_id}"
        )

        print(
            f"Disease   : "
            f"{latest_prediction['disease']}"
        )

        print(
            f"Confidence: "
            f"{latest_prediction['confidence']}"
        )

        print(
            f"Date      : "
            f"{latest_prediction['date']}"
        )

        print("=" * 60)

        return latest_prediction


    # =========================================================
    # GET ONE PREDICTION BY HISTORY ID
    #
    # THIS METHOD IS USED BY THE VIEW BUTTON
    # =========================================================

    @staticmethod
    def get_prediction_by_id(
        user_id,
        history_id
    ):

        conn = get_connection()

        if conn is None:

            print(
                "[ERROR] Database connection failed."
            )

            return None

        cursor = None

        try:

            cursor = conn.cursor()

            # -------------------------------------------------
            # IMPORTANT:
            #
            # We check BOTH:
            #     history_id
            #     user_id
            #
            # This prevents a logged-in user from viewing
            # another user's prediction by changing the URL.
            # -------------------------------------------------

            cursor.execute(
                """
                SELECT
                    history_id,
                    disease_name,
                    confidence,
                    symptoms,
                    prediction_date
                FROM prediction_history
                WHERE
                    history_id = :1
                    AND user_id = :2
                """,
                (
                    history_id,
                    user_id
                )
            )

            row = cursor.fetchone()

            # -------------------------------------------------
            # No prediction found
            # -------------------------------------------------

            if row is None:

                print(
                    f"[HISTORY] Prediction not found. "
                    f"History ID: {history_id}, "
                    f"User ID: {user_id}"
                )

                return None

            # -------------------------------------------------
            # Read symptoms
            # -------------------------------------------------

            symptoms_value = ""

            if row[3] is not None:

                try:

                    symptoms_value = row[3].read()

                except AttributeError:

                    symptoms_value = str(
                        row[3]
                    )

            # -------------------------------------------------
            # Create prediction dictionary
            # -------------------------------------------------

            prediction = {

                "history_id":
                    row[0],

                "disease":
                    row[1],

                "disease_name":
                    row[1],

                "confidence":
                    (
                        float(row[2])
                        if row[2] is not None
                        else None
                    ),

                "symptoms":
                    symptoms_value,

                "prediction_date":
                    row[4],

                "date":
                    row[4]
            }

            # -------------------------------------------------
            # Debug information
            # -------------------------------------------------

            print("=" * 60)
            print("PREDICTION DETAILS LOADED")
            print("=" * 60)

            print(
                f"History ID : "
                f"{prediction['history_id']}"
            )

            print(
                f"User ID    : "
                f"{user_id}"
            )

            print(
                f"Disease    : "
                f"{prediction['disease_name']}"
            )

            print(
                f"Confidence : "
                f"{prediction['confidence']}"
            )

            print(
                f"Symptoms   : "
                f"{prediction['symptoms']}"
            )

            print(
                f"Date       : "
                f"{prediction['prediction_date']}"
            )

            print("=" * 60)

            return prediction

        except Exception as e:

            print(
                "[ERROR] Could not get prediction by ID:"
            )

            print(e)

            return None

        finally:

            if cursor:

                try:
                    cursor.close()
                except Exception:
                    pass

            if conn:

                try:
                    conn.close()
                except Exception:
                    pass
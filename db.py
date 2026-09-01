import oracledb
from config import *

def get_connection():
    """
    Returns Oracle Database Connection
    """

    try:

        connection = oracledb.connect(

            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT,
            service_name=DB_SERVICE

        )

        return connection

    except Exception as e:

        print("Database Connection Error")
        print(e)

        return None


# ==========================
# Test Connection
# ==========================

if __name__ == "__main__":

    conn = get_connection()

    if conn:

        print("=" * 50)
        print(" Oracle Connected Successfully ")
        print("=" * 50)

        cursor = conn.cursor()

        cursor.execute("SELECT * FROM dual")

        print(cursor.fetchone())

        cursor.close()
        conn.close()

    else:

        print("Connection Failed")
import oracledb
from config import *

# ==========================================================
# Oracle Connection Pool
# ==========================================================
# A small pool avoids creating a brand-new Oracle connection
# for every request while still returning connections after use.

_pool = None


def init_pool():
    """Create the Oracle connection pool once for the Flask process."""
    global _pool

    if _pool is not None:
        return _pool

    try:
        _pool = oracledb.create_pool(
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT,
            service_name=DB_SERVICE,
            min=1,
            max=5,
            increment=1,
            getmode=oracledb.POOL_GETMODE_WAIT
        )

        print("Oracle Connection Pool Created Successfully")
        return _pool

    except Exception as e:
        print("Database Connection Pool Error")
        print(e)
        _pool = None
        return None


def get_connection():
    """Acquire a connection from the Oracle connection pool."""
    pool = init_pool()

    if pool is None:
        return None

    try:
        return pool.acquire()

    except Exception as e:
        print("Database Connection Error")
        print(e)
        return None


def close_connection(connection):
    """Return a connection to the pool instead of closing the pool itself."""
    if connection is None:
        return

    try:
        connection.close()
    except Exception as e:
        print("Database Connection Close Error")
        print(e)


def close_pool():
    """Close the pool when the application process is shutting down."""
    global _pool

    if _pool is not None:
        try:
            _pool.close()
            print("Oracle Connection Pool Closed")
        except Exception as e:
            print("Database Pool Close Error")
            print(e)
        finally:
            _pool = None


# ==========================================================
# Test Connection
# ==========================================================

if __name__ == "__main__":

    conn = get_connection()

    if conn:

        print("=" * 50)
        print(" Oracle Connected Successfully ")
        print("=" * 50)

        cursor = None

        try:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM dual")
            print(cursor.fetchone())
        finally:
            if cursor:
                cursor.close()
            close_connection(conn)
            close_pool()

    else:
        print("Connection Failed")

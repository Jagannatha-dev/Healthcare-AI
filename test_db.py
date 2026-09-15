from db import get_connection, close_connection, close_pool


def main():
    conn = get_connection()

    if conn is None:
        print("Oracle connection test FAILED")
        return 1

    cursor = None
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT SYS_CONTEXT('USERENV', 'SERVICE_NAME') FROM dual")
        service_name = cursor.fetchone()[0]
        print("Oracle connection test PASSED")
        print(f"Service: {service_name}")
        return 0
    except Exception as e:
        print("Oracle connection test FAILED")
        print(e)
        return 1
    finally:
        if cursor is not None:
            cursor.close()
        close_connection(conn)
        close_pool()


if __name__ == "__main__":
    raise SystemExit(main())

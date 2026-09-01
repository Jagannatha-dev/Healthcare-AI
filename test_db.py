from db import get_connection

connection = get_connection()

if connection:

    print("="*50)
    print("Oracle Connected Successfully")
    print("="*50)

    cursor = connection.cursor()

    cursor.execute("SELECT * FROM dual")

    print(cursor.fetchone())

    cursor.close()

    connection.close()

else:

    print("Connection Failed")
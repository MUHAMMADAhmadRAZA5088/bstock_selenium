import mysql.connector

# MySQL database connection details
connection = mysql.connector.connect(
    host="dbaas-db-4996826-do-user-21691157-0.f.db.ondigitalocean.com",         # ya aap ka host e.g., "127.0.0.1"
    user="doadmin",              # your MySQL username
    password="AVNS_Xf8UURLVY69Q2X4UO2q",              # your MySQL password
    database="Bstock",  # target database name
    port=25060
)

try:
    cursor = connection.cursor()
    
    # Table name to truncate
    table_name = "bstock_auctions"

    # Truncate the table
    cursor.execute(f"TRUNCATE TABLE {table_name};")

    connection.commit()
    print(f"Table `{table_name}` truncated successfully.")

except mysql.connector.Error as err:
    print(f"Error: {err}")

finally:
    if connection.is_connected():
        cursor.close()
        connection.close()

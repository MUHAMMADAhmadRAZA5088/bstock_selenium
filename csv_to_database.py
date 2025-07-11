import pandas as pd
import mysql.connector

# ✅ Step 1: CSV file load karo
df = pd.read_csv('all_output1.csv')  # Replace with your filename if different

# ✅ Step 2: MySQL connection banao
conn = mysql.connector.connect(
    host="dbaas-db-4996826-do-user-21691157-0.f.db.ondigitalocean.com",
    user="doadmin",
    password="AVNS_Xf8UURLVY69Q2X4UO2q",  # ← Change if your DB has password
    database="Bstock",  # ← Replace with your DB
    port = 25060
)
cursor = conn.cursor()

# ✅ Step 3: Table create karo (agar already nahi hai)
create_table_query = """
CREATE TABLE IF NOT EXISTS iphone_auctions (
    id INT PRIMARY KEY,
    title TEXT,
    current_bit VARCHAR(50),
    avergae_per_unit VARCHAR(50),
    address TEXT,
    close_in VARCHAR(50),
    close_date VARCHAR(100),
    minifest_url TEXT,
    minifest_status VARCHAR(50),
    url TEXT
)
"""
cursor.execute(create_table_query)

# ✅ Step 4: Insert data row-by-row
for _, row in df.iterrows():
    insert_query = """
    INSERT INTO iphone_auctions (id, title, current_bit, avergae_per_unit, address, close_in, close_date, minifest_url, minifest_status, url)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    cursor.execute(insert_query, (
        int(row['id']),
        row['title'],
        row['current_bit'],
        row['avergae_per_unit'],
        row['address'],
        row['close_in'],
        row['close_date'],
        row['minifest_url'],
        row['minifest_status'],
        row['url']
    ))

# ✅ Step 5: Save changes and close connection
conn.commit()
cursor.close()
conn.close()

print("🎉 Data inserted successfully!")

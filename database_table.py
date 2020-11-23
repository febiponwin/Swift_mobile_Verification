import sqlite3

conn = sqlite3.connect('database.db')
print ("Opened database successfully")

conn.execute('CREATE TABLE user_info (cws_id TEXT, phone_no TEXT, phone_model TEXT,created_time DATE, id TEXT)')
print ("Table created successfully")
conn.close()
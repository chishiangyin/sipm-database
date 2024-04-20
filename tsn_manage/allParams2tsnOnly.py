import sqlite3

# Connect to the original database
conn_original = sqlite3.connect('../all_sipms.db')
cursor_original = conn_original.cursor()

# Extract the desired data
cursor_original.execute('SELECT DISTINCT tsn, batch, box FROM csv')
rows = cursor_original.fetchall()

# Connect to the new database (this creates the file if it doesn't exist)
conn_new = sqlite3.connect('new_database.db')
cursor_new = conn_new.cursor()

# Create a new table in the new database
cursor_new.execute('''
CREATE TABLE IF NOT EXISTS TileSN (
    tsn INTEGER,
    batch INTEGER,
    box INTEGER
)
''')

# Insert the data into the new table
cursor_new.executemany('INSERT INTO TileSN (tsn, batch, box) VALUES (?, ?, ?)', rows)
conn_new.commit()

# Close all connections
cursor_original.close()
conn_original.close()
cursor_new.close()
conn_new.close()

print("Data transferred successfully!")


import sqlite3

def connect_db():
    """ Connect to the SQLite database. """
    return sqlite3.connect('new_database.db')

def add_index_column():
    """ Adds an 'index' column to the table and initializes it. """
    conn = connect_db()
    cursor = conn.cursor()

    # Check if the 'index' column already exists and add it if it doesn't
    cursor.execute("PRAGMA table_info(TileSN)")
    columns = cursor.fetchall()
    if 'num' not in [column[1] for column in columns]:
        cursor.execute("ALTER TABLE TileSN ADD COLUMN num INTEGER DEFAULT 0")
        print("Index column added.")
    else:
        print("Index column already exists.")

    # Fetch all tsn values to update the index
    cursor.execute("SELECT tsn FROM TileSN")
    all_tsn = cursor.fetchall()

    # Update the 'index' column with the last digit of 'tsn'
    for tsn in all_tsn:
        last_char = str(tsn[0])[-1]  # Extract the last character
        index_value = int(last_char)
        if index_value == 0:
            index_value = 10
        cursor.execute("UPDATE TileSN SET num = ? WHERE tsn = ?", (index_value, tsn[0]))

    conn.commit()
    conn.close()
    print("Index column initialized successfully.")
def main():
    add_index_column()

if __name__ == "__main__":
    main()

import sqlite3

def find_tsn_with_fewer_ch(cursor):
    # Query to find 'tsn' with fewer than 16 'ch' entries
    cursor.execute("""
        SELECT tsn, COUNT(DISTINCT ch) AS ch_count
        FROM csv
        GROUP BY tsn
        HAVING ch_count < 16
    """)
    results = cursor.fetchall()
    return results

# Connect to the destination SQLite database
dest_conn = sqlite3.connect('destination_database.db')
dest_cursor = dest_conn.cursor()

# Find tsn values that have less than 16 distinct ch values
tsn_fewer_ch = find_tsn_with_fewer_ch(dest_cursor)

# Print the results
if tsn_fewer_ch:
    print("TSN with fewer than 16 CH:")
    for tsn, count in tsn_fewer_ch:
        print(f"TSN: {tsn}, CH Count: {count}")
else:
    print("All TSNs have 16 or more CH.")

# Close the connection
dest_conn.close()


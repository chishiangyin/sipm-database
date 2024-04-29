import sqlite3

def unique_counts(cursor):
    # Query to count unique 'tsn'
    cursor.execute("SELECT COUNT(DISTINCT tsn) FROM csv")
    unique_tsn_count = cursor.fetchone()[0]

    # Query to count unique '(tsn, ch)' pairs using string concatenation
    cursor.execute("SELECT COUNT(DISTINCT tsn || ',' || ch) FROM csv")
    unique_tsn_ch_count = cursor.fetchone()[0]

    return unique_tsn_count, unique_tsn_ch_count

# Connect to the destination SQLite database
dest_conn = sqlite3.connect('destination_database.db')
dest_cursor = dest_conn.cursor()

# Get counts of unique 'tsn' and unique '(tsn, ch)' pairs
tsn_count, tsn_ch_count = unique_counts(dest_cursor)

print(f"Unique 'tsn' count: {tsn_count}")
print(f"Unique '(tsn, ch)' pairs count: {tsn_ch_count}")

# Close the connection
dest_conn.close()


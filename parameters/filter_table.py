import sqlite3

def get_create_table_statement(src_cursor, table_name):
    """ Generates a CREATE TABLE statement based on the source table schema """
    src_cursor.execute(f"PRAGMA table_info({table_name})")
    columns = src_cursor.fetchall()
    column_defs = ', '.join([f"{col[1]} {col[2]}" for col in columns])
    return f"CREATE TABLE IF NOT EXISTS {table_name} ({column_defs})"

# Connect to the source SQLite database
source_conn = sqlite3.connect('final_harvest.db')
source_cursor = source_conn.cursor()

# Connect to the destination SQLite database
dest_conn = sqlite3.connect('destination_database.db')
dest_cursor = dest_conn.cursor()

# Generate the CREATE TABLE statement from the source database
create_table_stmt = get_create_table_statement(source_cursor, 'csv')
dest_cursor.execute(create_table_stmt)

# Query to select rows, excluding those based on certain conditions
query = """
SELECT * FROM csv 
WHERE NOT (
    mu < 0.2 OR
    mu > 2.7 OR
    (run >= 426 and run <= 447) OR
    lambda > 0.7 OR
    lambda < 0.01 OR
    ndf < 3 OR
    alpha > 0.2 OR
    n_peaks < 3 OR
    prefit_gain < 6 OR
    fit_status IN (11, 12, 13) OR
    fit_status > 13 OR
    dcr <= 0 OR
    sigma0 < 3 OR
    sigma0 > 8 OR
    current > 3e-8
)
"""

# Execute the selection query on the source database
source_cursor.execute(query)
rows = source_cursor.fetchall()

# Insert the selected rows into the destination table
dest_cursor.executemany("INSERT INTO csv VALUES (" + ",".join(["?"] * len(rows[0])) + ")", rows)
dest_conn.commit()

# Close the connections
source_conn.close()
dest_conn.close()


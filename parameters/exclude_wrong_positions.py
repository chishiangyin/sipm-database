import sqlite3
import numpy as np
import sys

# Connect to the SQLite database
conn = sqlite3.connect(sys.argv[1])  # Make sure the path is correct

# Create a cursor object using the cursor method
cursor = conn.cursor()

# SQL query to fetch distinct runs
query = """
SELECT DISTINCT run
FROM csv
WHERE match_x > 6 OR match_y < -6;
"""

# Execute the query
cursor.execute(query)

# Fetch all results
excluded_runs = cursor.fetchall()
print(excluded_runs)

excluded_runs = list(map(lambda x: int(x[0]), excluded_runs))
excluded_runs.sort()
# Print the list of excluded runs
print("Excluded runs based on condition (match_x > 6 AND match_y < -6):")
for run in excluded_runs:
    print(run)  # Each run is a tuple, print the first element

# Close the connection to the database
conn.close()


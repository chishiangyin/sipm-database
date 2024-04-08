import os
import sys
import sqlite3
import csv


path = sys.argv[1]
if len(sys.argv)>2:
    database_path = sys.argv[2]
elif not os.path.isfile('sipm_database.db'):
    database_path = 'sipm_database.db'
else:
    answer = input("sipm_database.db already exists. delete? (Y/N)").upper()
    if answer == 'Y':
        os.system('rm sipm_database.db')
        database_path = 'sipm_database.db'
    else:
        exit()
# Connect to the SQLite3 database
conn = sqlite3.connect(database_path)
cursor = conn.cursor()

table_name = os.path.splitext(os.path.basename(path))[0]

def get_column_names_and_types(cursor, file_path):
    """
    Retrieves the column names and data types from the first row of the CSV file.
    """
    with open(file_path, 'r') as csv_file:
        csv_reader = csv.reader(csv_file)
        headers = next(csv_reader)

        # Determine the data types for each column
        column_types = []
        for row in csv_reader:
            for i, value in enumerate(row):
                try:
                    float(value)
                    column_types.append('REAL')
                    break
                except ValueError:
                    column_types.append('TEXT')
                    break

    return headers, column_types

def process_csv_file(file_path, common_headers, table_name):
    """
    Processes a CSV file and adds its data to the SQLite3 database.
    """
    with open(file_path, 'r') as csv_file:
        csv_reader = csv.reader(csv_file)
        headers = next(csv_reader)  # Get the column headers
        headers, column_types = get_column_names_and_types(cursor, file_path)
        print(headers)
        print(column_types)

        # Check if the headers are consistent with the common headers
        if not common_headers is None:
            missing_headers = [h for h in common_headers if h not in headers]
            extra_headers = [h for h in headers if h not in common_headers]
        else:
            missing_headers = None
            extra_headers = None

        if not missing_headers and not extra_headers:
            # Create the table with the appropriate column names
            #cursor.execute(f"CREATE TABLE IF NOT EXISTS {table_name} ({', '.join([f'{h} TEXT' for h in headers])})")
            create_table_query = f"CREATE TABLE IF NOT EXISTS {table_name} ({', '.join([f'{h} {t}' for h, t in zip(headers, column_types)])})"
            cursor.execute(create_table_query)
  

            # Insert the data into the table
            for row in csv_reader:
                #cursor.execute(f"INSERT INTO {os.path.splitext(os.path.basename(file_path))[0]} ({', '.join(headers)}) VALUES ({', '.join(['?' for _ in headers])})", row)
                cursor.execute(f"INSERT INTO {table_name} ({', '.join(headers)}) VALUES ({', '.join(['?' for _ in headers])})", row)
        else:
            if missing_headers:
                print(f"Skipping file \033[1;93m{file_path}\033[0m with missing columns: \033[1;96m{', '.join(missing_headers)}\033[0m")
            if extra_headers:
                print(f"Skipping file \033[1;93m{file_path}\033[0m with extra columns: \033[1;96m{', '.join(extra_headers)}\033[0m")

def process_directory(directory_path, table_name):
    """
    Processes all CSV files in a directory and adds their data to the SQLite3 database.
    """
    common_headers = None

    for filename in os.listdir(directory_path):
        if filename.endswith('.csv'):
            file_path = os.path.join(directory_path, filename)

            # Get the column headers for the first file
            if common_headers is None:
                with open(file_path, 'r') as csv_file:
                    csv_reader = csv.reader(csv_file)
                    common_headers = next(csv_reader)

            process_csv_file(file_path, common_headers, table_name)


# Check if the path is a file or directory
if os.path.isfile(path):
    if path.endswith('.csv'):
        process_csv_file(path, None, table_name)
    else:
        print(f"{path} is not a CSV file.")
elif os.path.isdir(path):
    process_directory(path,table_name)
else:
    print(f"{path} is not a valid file or directory.")

# Commit the changes and close the connection
conn.commit()
conn.close()

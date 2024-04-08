import sqlite3
from predefined_colors import *

def get_column_names(cursor, table_name):
    """
    Retrieves the column names for the given table.
    """
    cursor.execute(f"PRAGMA table_info({table_name})")
    return [row[1] for row in cursor.fetchall()]

def print_available_keywords():
    """
    Prints the available keywords for the user to interact with.
    """
    print(f'{BIBlue}'"Available keywords:"f'{Color_Off}')
    print("- "f'{BIYellow}'"col\033[0m  Prints all column names"f'{Color_Off}')
    print("- "f'{BIYellow}'"show\033[0m  Allows you to select and display rows based on conditions"f'{Color_Off}')
    print("- "f'{BIYellow}'"exit,q\033[0m  Exits the program"f'{Color_Off}')

def show_values(cursor, table_name):
    """
    Allows the user to select and display rows based on conditions.
    """
    column_names = get_column_names(cursor, table_name)
    print("Select the columns you want to display (comma-separated):")
    selected_columns = input().split(",")

    # Validate the selected columns
    for column in selected_columns:
        if column.strip() not in column_names:
            print(f"Error: {column.strip()} is not a valid column name.")
            return

    print("Enter the selection conditions (e.g., column1 > 3 and column5 == 4):")
    selection_conditions = input().split(" and ")

    # Build the SQL query
    query = f"SELECT {', '.join(selected_columns)} FROM {table_name} WHERE "
    query += " AND ".join(selection_conditions)

    header_str = '\033[1;93m'
    first = 0
    for col in column_names:
        if not first==0:
            header_str += '\t'
        first += 1
        header_str += f'{col}'
    header_str += '\033[0m'
    print(header_str)
    # Execute the query and print the results
    cursor.execute(query)
    rows = cursor.fetchall()
    for row in rows:
        row_str = ''
        first = 0
        for col in row:
            if not first==0:
                row_str += '\t'
            first += 1
            row_str += f'{col}'
        print(row_str)

def main():
    # Connect to the SQLite3 database
    conn = sqlite3.connect('sipm_database.db')
    cursor = conn.cursor()

    # Get the table name
    # Execute a query to retrieve the table names
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")

    # Fetch all results
    table_names = cursor.fetchall()
    print(f'{BIBlue}'"Available tables:"f'{Color_Off}')
    for name in table_names:
        print(f'\033[1;92m{name[0]}\033[0m')
    print("Enter the table name:")
    table_name = input()
    if table_name == "q" or table_name == 'exit':
        exit()

    while True:
        print_available_keywords()
        print("Enter a keyword or 'exit' to quit:")
        keyword = input().lower()

        if keyword == "col":
            column_names = get_column_names(cursor, table_name)
            print("Column names:")
            for column in column_names:
                print(column)
        elif keyword == "show":
            show_values(cursor, table_name)
        elif keyword == "exit":
            break
        elif keyword == "q":
            break
        else:
            print("Invalid keyword. Please try again.")

    # Close the database connection
    conn.close()

if __name__ == "__main__":
    main()

import sqlite3
from predefined_colors import *
import os, sys

db_path = sys.argv[1]

def connect_db(db_path):
    """ Connect to the SQLite database or create it if it doesn't exist. """
    db_exists = os.path.exists(db_path)
    conn = sqlite3.connect(db_path)
    if not db_exists:
        initialize_database(conn)
    return conn

def initialize_database(conn):
    """ Initialize the database with the required table and columns. """
    cursor = conn.cursor()
    # Create the TileSN table if it does not exist
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS TileSN (
            tsn TEXT PRIMARY KEY,
            batch INTEGER,
            box INTEGER,
            num INTEGER
        )
    """)
    conn.commit()
    print("Database initialized and table 'TileSN' created.")
def get_index(alist, num):
    for i in range(len(alist)):
        if num== alist[i]:
            return i
        else:
            continue
def find_batch_box(tsn):
    """ Given a TSN, find the corresponding batch and box. """
    conn = connect_db(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT batch, box, num FROM TileSN WHERE tsn = ?", (tsn,))
    result = cursor.fetchone()
    conn.close()
    if result:
        batch_box_str = f"{result[0]}-{result[1]}-{result[2]}"
    else:
        batch_box_str = None
    return batch_box_str

def find_tsn_by_batch_box(batch, box):
    """ Given a batch and box, find all related TSNs. """
    conn = connect_db(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT num, tsn FROM TileSN WHERE batch = ? AND box = ?", (batch, box))
    results = cursor.fetchall()
    conn.close()
    # Create a list of tuples (num, tsn)
    num_tsn_list = [(result[0], result[1]) for result in results]

    # Sort the list by 'num' (the first element of the tuple)
    sorted_num_tsn_list = sorted(num_tsn_list, key=lambda x: x[0])

    # If you need only the tsn list in sorted order:
    sorted_tsn_list = [(num, tsn) for num, tsn in sorted_num_tsn_list]
    return sorted_tsn_list

def change_row(tsn, new_batch, new_box, new_num):
    """ Change the batch and box for a given tsn. Display old values for confirmation. """
    conn = connect_db(db_path)
    cursor = conn.cursor()
    
    # Fetch old values
    old_values = find_batch_box(tsn)
    if not old_values:
        print(f"Change from None to ({new_batch}, {new_box}, {new_num}, {tsn})?")
        confirmation = input("Confirm update (yes/no)? ")

        if confirmation.lower() == 'yes':
            # Update the row
            print(new_batch, new_box, new_num, tsn)
            cursor.execute("INSERT OR REPLACE INTO TileSN (tsn, batch, box, num) VALUES (?, ?, ?, ?)", (tsn, new_batch, new_box, new_num))
            conn.commit()
            print("Row updated successfully.")
        else:
            print("Update cancelled.")
    else:
        old_values = old_values.strip().split("-")
        
        print(f"Change from ({old_values[0]}, {old_values[1]}, {old_values[2]}, {tsn}) to ({new_batch}, {new_box}, {new_num}, {tsn})?")
        confirmation = input("Confirm update (yes/no)? ")

        if confirmation.lower() == 'yes':
            # Update the row
            cursor.execute("UPDATE TileSN SET batch = ?, box = ?, num = ? WHERE tsn = ?", (new_batch, new_box, new_num, tsn))
            conn.commit()
            print("Row updated successfully.")
        else:
            print("Update cancelled.")
        
    conn.close()

def main():
    while True:
        print(f"\n{BIYellow}Options:{Color_Off}")
        print(f"{BIPurple}1. Find batch and box by TSN")
        print(f"{BIBlue}2. Find TSNs by batch and box")
        print(f"{BIGreen}3. Change a row")
        print(f"{BIRed}4. Exit{Color_Off}")
        choice = input(f"{BICyan}Enter choice:{Color_Off} ")
        
        if choice == '1':
            tsn = input(f"{BICyan}Enter TSN:{Color_Off} ")
            result = find_batch_box(tsn)
            print(f"{BIYellow}Result:", result if result else f"{BIRed}No data found.{Color_Off}")
        
        elif choice == '2':
            batch_box = input("Enter batch-box: ")
            batch = int(batch_box.split("-")[0])
            box = int(batch_box.split("-")[1])
            results = find_tsn_by_batch_box(batch, box)
            num = [result[0] for result in results]
            tsn = [result[1] for result in results]
            if results:
                for i in range(1,11):
                    if i in num:
                        print(i, tsn[get_index(num, i)])
                    else:
                        print(i, f'{BIRed}None{Color_Off}')
            else:
                print('None.')
        
        elif choice == '3':
            tsn = input("Enter TSN: ")
            if tsn == '':
                continue
            result = find_batch_box(tsn)
            print(f"{BIYellow}Result:", result if result else f"{BIRed}No data found.{Color_Off}")
            batch_box = input("Enter batch-box: ")
            if batch_box == '':
                continue
            new_batch = int(batch_box.split("-")[0])
            new_box = int(batch_box.split("-")[1])
            if len(batch_box.split("-")) > 2:
                new_num = batch_box.split("-")[2]
                change_row(tsn, new_batch, new_box, new_num)
            else:
                new_num = int(str(tsn)[-1]) if int(str(tsn)[-1]) != 0 else 10
                change_row(tsn, new_batch, new_box, new_num)
        
        elif choice == '4':
            print("Exiting...")
            break

        else:
            print("Invalid choice, please try again.")

if __name__ == "__main__":
    main()


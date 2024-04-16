import sqlite3
import datetime

# Get current time
current_time = datetime.datetime.now()

# Assuming your database supports SQL's DATETIME format
# Convert the current time to a string in the appropriate format
current_time_str = current_time.strftime('%Y-%m-%d %H:%M:%S')

def print_all_patient_entries():
    try:
        conn = sqlite3.connect('site.db')
        cursor = conn.cursor()

        # Select all records from the patient_entries table
        query = "SELECT sickness_info FROM patient_entries WHERE username = ? AND time <= ? ORDER BY time DESC LIMIT 1"
        # cursor.execute('SELECT sickness_info FROM patient_entries WHERE username = ?', ('igniters',))
        # cursor.execute('SELECT * FROM patient_entries WHERE username = ?', ('igniters',))
        cursor.execute(query, ('igniters', current_time_str))
        

        
        # Fetch all the selected records
        records = cursor.fetchone()

        # Print the selected records
        for record in records:
            print(record)
            # for string in record:
            #     cleaned_string = string.strip()
            #     print(cleaned_string)

        print("All records from patient_entries table printed successfully.")

    except sqlite3.Error as e:
        print(f"Error selecting records: {e}")

    finally:
        if conn:
            conn.close()

# Call the function to print all records
print_all_patient_entries()

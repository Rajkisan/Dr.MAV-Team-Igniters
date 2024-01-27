import sqlite3

def print_all_patient_entries():
    try:
        conn = sqlite3.connect('site.db')
        cursor = conn.cursor()

        # Select all records from the patient_entries table
        cursor.execute('SELECT * FROM patient_entries')
        
        # Fetch all the selected records
        records = cursor.fetchall()

        # Print the selected records
        for record in records:
            print(record)

        print("All records from patient_entries table printed successfully.")

    except sqlite3.Error as e:
        print(f"Error selecting records: {e}")

    finally:
        if conn:
            conn.close()

# Call the function to print all records
print_all_patient_entries()

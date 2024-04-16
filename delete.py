import sqlite3

def print_last_patient_entry_for_user(username):
    try:
        conn = sqlite3.connect('site.db')
        cursor = conn.cursor()

        # Select the last record for the specified username ordered by date and time
        query = "SELECT * FROM patient_entries WHERE username=? ORDER BY date DESC, time DESC LIMIT 1"
        cursor.execute(query, (username,))
        
        # Fetch the selected record
        record = cursor.fetchone()

        # Print the selected record
        if record:
            print("Last response for user '{}' ordered by date and time:".format(username))
            print(record)
        else:
            print("No response found for user '{}'.".format(username))

    except sqlite3.Error as e:
        print(f"Error selecting record: {e}")

    finally:
        if conn:
            conn.close()

# Call the function to print the last response for the specified user ordered by date and time
print_last_patient_entry_for_user('igniters')

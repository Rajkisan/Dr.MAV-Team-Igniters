from g4f.client import Client
import re
import os
import sqlite3
import datetime

def print_all_patient_entries(records):
    try:
        conn = sqlite3.connect('site.db')
        cursor = conn.cursor()
        username='igniters'
        # Get current time
        current_time = datetime.datetime.now()
        current_time_str = current_time.strftime('%Y-%m-%d %H:%M:%S')
        print(current_time_str)

        # Select all records from the patient_entries table
        query = "SELECT sickness_info FROM patient_entries WHERE username=? ORDER BY date DESC, time DESC LIMIT 1"
        cursor.execute(query, (username,))

        # Fetch the selected records
        records = cursor.fetchone()

        # Print the selected records
        for record in records:
            print(record)

        print("All records from patient_entries table printed successfully.")

        return records  # Return records for further use

    except sqlite3.Error as e:
        print(f"Error selecting records: {e}")

    finally:
        if conn:
            conn.close()

# Define the variable records
records = None

# Call the function to print all records and retrieve records
records = print_all_patient_entries(records)

# Define the path to the static folder
static_folder = "static"

# Create the static folder if it doesn't exist
if not os.path.exists(static_folder):
    os.makedirs(static_folder)

# Patient description
patient_description = records

# Prompt for GPT-3
prompt = f"Patient is suffering from {patient_description}. What are the list of 10 possible prescreening questions asked by the doctor to them like how many days you have fever and do you have cough, cold? and the questions should be of yes or no type"

# Call GPT-3 to generate response
client = Client()
response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[{"role": "user", "content": prompt}],
)

# Convert response to string
response = str(response.choices[0].message.content)
print(response)

# Extract questions using regex
question_pattern = r'\*\*(.*?)\*\*'
questions = re.findall(question_pattern, response, re.DOTALL)

# Prepare JavaScript code
js_code = "const questions = [\n"
for index, question in enumerate(questions):
    js_code += f"  {{\n"
    js_code += f"    question: \"{question}\",\n"
    js_code += f"    answer: 1, // Set the correct answer index here\n"
    js_code += f"  }},\n"
js_code += "];\n"

# Write the JavaScript code to a file in the static folder
js_file_path = os.path.join(static_folder, "questions.js")
with open(js_file_path, "w") as js_file:
    js_file.write(js_code)

print(f"questions.js file created at: {js_file_path}")

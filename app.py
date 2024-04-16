from flask import Flask, render_template, request, jsonify, redirect, url_for, flash, session, g
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'


def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect('site.db')
        g.db.row_factory = sqlite3.Row
    return g.db

# Add this route for the 'frame' endpoint


# Create the database table for patient entries
conn = sqlite3.connect('site.db')
cursor = conn.cursor()
cursor.execute('''
    CREATE TABLE IF NOT EXISTS patient_entries (
        id INTEGER PRIMARY KEY,
        patient_id INTEGER,
        username TEXT,
        sickness_info TEXT NOT NULL,
        time TEXT,
        date TEXT,
        FOREIGN KEY(patient_id) REFERENCES users(id)
    )
''')
conn.commit()
conn.close()

# Database initialization for users
def init_db():
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            password TEXT NOT NULL,
            user_type TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

init_db()

# Signup route
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user_type = request.form['user_type']

        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()

        # Check if the username already exists
        cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
        if cursor.fetchone():
            flash('Username already exists. Please choose a different one.', 'error')
            conn.close()
            return redirect(url_for('signup'))

        # Use the default hashing method
        hashed_password = generate_password_hash(password)
        print(hashed_password)

        # Insert the new user into the database
        cursor.execute('INSERT INTO users (username, password, user_type) VALUES (?, ?, ?)',
                       (username, hashed_password, user_type))
        conn.commit()
        conn.close()

        flash('Account created successfully. Please login.', 'success')
        return redirect(url_for('login'))

    return render_template('signup.html')


# Submit Sickness Info route for patients
@app.route('/submit_sickness_info', methods=['POST'])
def submit_sickness_info():
    if 'user_type' in session and session['user_type'] == 'Patient':
        sickness_info = request.form['sickness_info']


        # Store the sickness information in the database for the patient
        # patient_id = session.get('user_id')

        
        conn = get_db()
        cursor = conn.cursor()

            # Get the current time and date
        current_time = datetime.now().strftime("%H:%M:%S")
        current_date = datetime.now().strftime("%Y-%m-%d")

            # Remove the username parameter and allow multiple entries for the same patient
        cursor.execute('INSERT INTO patient_entries (username, sickness_info, time, date) VALUES (?, ?, ?, ?)',
                        (session['username'], sickness_info, current_time, current_date))
        conn.commit()
        conn.close()
        print("Uploaded Successfully")

        return jsonify({'message': 'Sickness information submitted successfully'})
       
    else:
        return jsonify({'error': 'Unauthorized access'})


# Update doctor's dashboard with sickness entries
@app.route('/get_sickness_entries', methods=['GET'])
def get_sickness_entries():
    conn = get_db()
    cursor = conn.cursor()

    # Fetch sickness information from patient_entries
    cursor.execute('SELECT username, sickness_info, time, date FROM patient_entries')
    sickness_entries = cursor.fetchall()

    conn.close()

    return render_template('dashboard_doctor_entries.html', sickness_entries=sickness_entries)

# Login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()

        # Check if the username exists
        cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
        user = cursor.fetchone()

        conn.close()

        if user and check_password_hash(user[2], password):
            flash('Login successful!', 'success')
            print(password)
            session['user_type'] = user[3]
            session['user_id'] = user[0]
            session['username'] = user[1]
            return redirect(url_for('dashboard', user_type=user[3]))
        else:
            flash('Login failed. Check your username and password.', 'error')

    return render_template('login.html')
    

# Logout route
@app.route('/logout')
def logout():
    session.pop('user_type', None)
    session.pop('user_id', None)
    session.pop('username', None)
    flash('You have been logged out.', 'success')
    return redirect(url_for('home'))

# Dashboard route (protected route, user must be logged in)
@app.route('/dashboard/<user_type>', methods=['GET', 'POST'])
def dashboard(user_type):
    if 'user_type' not in session or session['user_type'] != user_type:
        flash('Please log in to access the dashboard.', 'error')
        return redirect(url_for('login'))

    if user_type == 'Patient':
        if request.method == 'POST':
            sickness_info = request.form['sickness_info']
            flash(f'Sickness information submitted: {sickness_info}', 'success')
        return render_template('dashboard_patient.html', user_type=user_type)
    elif user_type == 'Doctor':
        return render_template('dashboard_doctor.html', user_type=user_type)

# Route for previous visit
@app.route('/previous_visit')
def previous_visit():
    return render_template('previous_visit.html')

# Route for medicine brought
@app.route('/medicine_brought')
def medicine_brought():
    return render_template('medicine_brought.html')

# Default route with navbar
@app.route('/')
def home():
    return render_template('home.html')


# Default route with navbar
@app.route('/index')
def index():
    return render_template('index.html')

def show_game():
    # Add logic to fetch quizzes data and pass it to the template
    game_data = get_game_data()  # Replace with your logic to fetch quizzes data
    return render_template('game.html', game=game_data)

@app.route('/frame')
def frame():
    return render_template('frame.html')

# Add this route for the 'framedoc' endpoint
@app.route('/framedoc')
def framedoc():
    return render_template('framedoc.html')
# Default route with navbar
@app.route('/game')
def game():
    return render_template('game.html')
@app.route('/delete_entry', methods=['POST'])
def delete_entry():
    username = request.form['username']
    time = request.form['time']
    date = request.form['date']

    conn = get_db()
    cursor = conn.cursor()

        # Delete the entry with the specified username
    cursor.execute('DELETE FROM patient_entries WHERE username = ? AND time = ? AND date = ?', (username, time, date))
    print("Deleted Successfully")
    conn.commit()
    conn.close()

    return jsonify({'message': 'Sickness information deleted successfully'})



if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True)

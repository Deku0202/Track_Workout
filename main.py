# Importing flask module in the project is mandatory
# An object of Flask class is our WSGI application.
from flask import Flask, flash, redirect, render_template, request, session
from werkzeug.security import check_password_hash, generate_password_hash
import sqlite3
from flask_login import UserMixin
from datetime import datetime
import requests


# from helper import login_required, lookup, look, rating

# Flask constructor takes the name of 
# current module (__name__) as argument.
app = Flask(__name__)
app.secret_key = "deku"


# Connect db
conn = sqlite3.connect("database.db", check_same_thread=False)
db = conn.cursor()


@app.route("/logout")
# @login_required
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")

# the associated function.
@app.route('/')
def main():
    if len(session) != 1:
        return redirect("/register")

    else:
        return render_template("workout.html")

@app.route('/login', methods=["GET", "POST"])
def login():
    
    #User will reach to login via post method
    if request.method == "POST":
        #get form data
        username = request.form.get("username")
        password = request.form.get("password")
        
        #return back to samepage if there is no input 
        if not username or not password:
            return render_template("login.html")
        
        #Ensure both username and password are correct 
        info = db.execute("SELECT * FROM users WHERE username = ?", (username,)).fetchone()

        #Checking if user exist and password is correct 
        if info is None or not check_password_hash(info[2], password):
            return render_template("login.html")
        
        #Remember User Sessoins
        session["user_id"] = info[0]
        
        #Redirect to home page after login
        return redirect("/")
    else:
        if "user" in session:
            return redirect("/")
        
        return render_template("login.html")

@app.route('/register', methods=["GET","POST"])
def register():
    if request.method == "POST":
        
        #get form data
        username = request.form.get("username")
        password = request.form.get("password")
        
        #return back to samepage if there is no input 
        if not username or not password:
            return render_template("signup.html")

        # #check no same name
        name = db.execute("SELECT username FROM users WHERE username = ?", (username,)).fetchone()
        if name is not None:
            return render_template("signup.html")
        
        #generate password in hash 
        pwhash = generate_password_hash(password, method='pbkdf2:sha256', salt_length=8)
        
        #insert the user_data into the database 
        db.execute("INSERT INTO users (username, password) VALUES(?, ?)", (username, pwhash))
        conn.commit()
        
        return redirect("/login")
        
    return render_template("signup.html")

@app.route('/start_session', methods=["POST"])
def history():
    
    if request.method == "POST":
        
        #get today date
        today = datetime.today().strftime('%Y-%m-%d')
        
        #insert into history
        db.execute("INSERT INTO History (user_id, total_time, date) VALUES(?, ?, ?)", (session['user_id'], 0, today))
        conn.commit()

# Used this function to add the data from api since I'm just going to use local database 
# @app.route('/sync_exercise')
# def sync():
    
#     url = "https://exercise-db-fitness-workout-gym.p.rapidapi.com/exercises"
    
#     headers = {
#         "X-RapidAPI-Key": "d596432b2fmshd5d8561a785da4cp101137jsna77be07b5a68",
#         "X-RapidAPI-Host": "exercise-db-fitness-workout-gym.p.rapidapi.com"
#     }
    
#     response = requests.get(url, headers=headers)
#     response.raise_for_status()
#     exercises = response.json()
#     exercises_ids = exercises.get("excercises_ids", [])

#     for ex_id in exercises_ids:
#         # Step 2: Fetch details for each exercise
#         detail_url = f"https://exercise-db-fitness-workout-gym.p.rapidapi.com/exercise/{ex_id}"
#         detail_resp = requests.get(detail_url, headers=headers)
#         detail_resp.raise_for_status()
#         detail = detail_resp.json()

#         name = detail.get("name")
#         if not name:
#             continue

#         # Insert Exercise
#         db.execute("INSERT OR IGNORE INTO Exercise (name) VALUES (?)", (name,))
#         db.execute("SELECT exercise_id FROM Exercise WHERE name = ?", (name,))
#         exercise_db_id = db.fetchone()[0]

#         # Insert primary muscles
#         for muscle_name in detail.get("primaryMuscles", []):
#             db.execute("INSERT OR IGNORE INTO Muscle (name) VALUES (?)", (muscle_name,))
#             db.execute("SELECT muscle_id FROM Muscle WHERE name = ?", (muscle_name,))
#             muscle_id = db.fetchone()[0]

#             db.execute("""
#                 INSERT OR IGNORE INTO ExerciseMuscle (exercise_id, muscle_id, role)
#                 VALUES (?, ?, 'primary')
#             """, (exercise_db_id, muscle_id))

#         # Insert secondary muscles
#         for muscle_name in detail.get("secondaryMuscles", []):
#             db.execute("INSERT OR IGNORE INTO Muscle (name) VALUES (?)", (muscle_name,))
#             db.execute("SELECT muscle_id FROM Muscle WHERE name = ?", (muscle_name,))
#             muscle_id = db.fetchone()[0]

#             db.execute("""
#                 INSERT OR IGNORE INTO ExerciseMuscle (exercise_id, muscle_id, role)
#                 VALUES (?, ?, 'secondary')
#             """, (exercise_db_id, muscle_id))

#         conn.commit()

#     conn.close()
    
# main driver function
if __name__ == '__main__':

    # run() method of Flask class runs the application 
    # on the local development server.
    app.run()
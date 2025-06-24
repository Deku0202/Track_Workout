# Importing flask module in the project is mandatory
# An object of Flask class is our WSGI application.
from flask import Flask, flash, redirect, render_template, request, session
from werkzeug.security import check_password_hash, generate_password_hash
import sqlite3
from flask_login import UserMixin
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
        return render_template("home.html")

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
    
# main driver function
if __name__ == '__main__':

    # run() method of Flask class runs the application 
    # on the local development server.
    app.run()
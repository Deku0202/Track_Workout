# Importing flask module in the project is mandatory
# An object of Flask class is our WSGI application.
from flask import Flask, flash, redirect, render_template, request, session
from flask_login import UserMixin
import sqlite3

# Flask constructor takes the name of 
# current module (__name__) as argument.
app = Flask(__name__)

# Configure SQLite database

# Connect db
conn = sqlite3.connect("database.db", check_same_thread=False)
db = conn.cursor()


# The route() function of the Flask class is a decorator, 
# which tells the application which URL should call 
# the associated function.
@app.route('/')
def main():
    return render_template("home.html")

@app.route('/login')
def login():
    return render_template("login.html")

@app.route('/regisiter', methods=["GET","POST"])
def regisiter():
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
        
        
        #insert the user_data into the database 
        db.execute("INSERT INTO users (username, password) VALUES(?, ?)", (username, password))
        conn.commit()
        
        return redirect("/login")
        
    return render_template("signup.html")
    
# main driver function
if __name__ == '__main__':

    # run() method of Flask class runs the application 
    # on the local development server.
    app.run()
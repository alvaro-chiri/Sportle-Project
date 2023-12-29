import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, jsonify
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
import random

from helpers import apology, login_required, lookup

# Configure application
app = Flask(__name__)

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///sportle.db")
# CHANGE THE ABOVE TO THE CORRECT DB LATER

#KEEP
@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

#KEEP BUT CHANGE AS THIS WILL BE THE HOMEPAGE AFTER LOGIN
@app.route("/")
def index():
    """Shows Register or Login button"""
    # user = db.execute("SELECT * FROM users WHERE id = ?", session["user_id"])

    return render_template("index.html")

# Make the game
@app.route("/play", methods=["GET", "POST"])
# @login_required
def play():
    """Build the game"""
    teams = db.execute("SELECT * FROM teams")
    
    if teams:
        teams = sorted(teams, key=lambda x: x['teamName'])

        random_team = random.choice(teams)

        return render_template("play.html", random_team=random_team, teams=teams)

    return render_template("play.html", teams=teams)

# @app.route("/user_answer", methods=["GET"])
# def user_answer():
#     """get the users answer for the game"""
#     user_answer = request.args.get("user_answer")

#     submitted_team = db.execute(
#         "SELECT * FROM teams WHERE teamName = ?", request.form.get("user_answer")
#     ).fetchone()

#     return jsonify(submitted_team)

# if __name__ == "__main__":
#     app.run(debug=True)


#NEED
@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute(
            "SELECT * FROM users WHERE username = ?", request.form.get("username")
        )

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(
            rows[0]["passwordHash"], request.form.get("password")
        ):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")

#NEED
@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


#NEED
@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    # User reached route via POST
    if request.method == "POST":
        # user must give username and password
        if not request.form.get("username"):
            return apology("must provide username", 400)
        elif not request.form.get("password"):
            return apology("must provide password", 400)
        elif not request.form.get("confirmation"):
            return apology("must provide confirmation", 400)

        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        if not password == confirmation:
            return apology("passwords must match", 400)

        rows = db.execute(
            "SELECT * FROM users WHERE username = ?", request.form.get("username")
        )

        # make sure username doesn't exist yet
        if len(rows) != 0:
            return apology("this username is already in use", 400)

        # create user
        db.execute(
            "INSERT INTO users (username, passwordHash) VALUES(?, ?)",
            username,
            generate_password_hash(password, method="pbkdf2"),
        )

        get_user = db.execute(
            "SELECT * FROM users WHERE username = ?", request.form.get("username")
        )

        session["user_id"] = get_user[0]["id"]

        flash("Registered!")
        return redirect("/")

    else:
        return render_template("register.html")

#KEEP
@app.route("/changePassword", methods=["GET", "POST"])
def changePassword():
    """Change Password"""
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure password was submitted
        if not request.form.get("password"):
            return apology("must provide password", 403)
        elif not request.form.get("new_password"):
            return apology("must provide new password", 403)
        elif not request.form.get("confirmation"):
            return apology("must provide confirmation", 403)

        password = request.form.get("password")
        new_password = request.form.get("new_password")
        confirmation = request.form.get("confirmation")

        if not new_password == confirmation:
            return apology("passwords must match", 403)

        # Query database for user
        rows = db.execute("SELECT * FROM users WHERE id = ?", session["user_id"])

        # Ensure password is correct
        if not check_password_hash(rows[0]["passwordHash"], password):
            return apology("invalid password", 403)

        # update passwordHash with new passwordHash (new password)
        db.execute(
            "UPDATE users SET passwordHash = ? WHERE id = ?",
            generate_password_hash(new_password, method="pbkdf2"),
            session["user_id"],
        )

        # Redirect user to home page
        flash("Password Changed!")
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("changePassword.html")
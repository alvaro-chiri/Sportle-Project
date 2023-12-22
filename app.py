import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""
    portfolio = db.execute(
        "SELECT * FROM portfolio WHERE user_id = ?", session["user_id"]
    )
    user = db.execute("SELECT * FROM users WHERE id = ?", session["user_id"])

    cash = user[0]["cash"]

    if portfolio != 0:
        total = 0
        for stock in portfolio:
            curr = lookup(stock["symbol"])
            stock["price"] = curr["price"]
            amount = stock["shares"]

            price = curr["price"]

            total = total + (price * amount)
        total = total + cash

        return render_template(
            "index.html", portfolio=portfolio, cash=cash, total=total
        )

    return render_template("index.html", cash=cash, total=total)


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    if request.method == "POST":
        # make sure that they inputed a ticker and an amount
        try:
            shares = int(request.form.get("shares"))
        except ValueError:
            return apology("amount must be a positive integer", 400)

        symbol = request.form.get("symbol")
        amount = request.form.get("shares")
        if not symbol:
            return apology("please enter a symbol")
        elif not amount or int(amount) < 0:
            return apology("enter an amount")

        # make sure stock exists
        stock = lookup(request.form.get("symbol"))

        if not stock:
            return apology("Stock doesn't exist")

        name = stock["name"]
        price = stock["price"]
        symbol = stock["symbol"]

        # calculate the total cost of buying
        total = price * float(amount)

        user = db.execute("SELECT * FROM users WHERE id = ?", session["user_id"])

        username = user[0]["username"]
        cash = user[0]["cash"]

        if total > cash:
            return apology("You do not have enough cash")

        # check if portfolio db has this stock under the user_id

        portfolio_check = db.execute(
            "SELECT * FROM portfolio WHERE user_id = ? and name = ?",
            session["user_id"],
            name,
        )

        if len(portfolio_check) != 0:
            # if this has a result update the values
            portfolio_id = portfolio_check[0]["id"]
            portfolio_name = portfolio_check[0]["name"]
            p_shares = portfolio_check[0]["shares"]
            p_total = portfolio_check[0]["total"]

            new_shares = p_shares + int(amount)
            new_total = total + p_total
            db.execute(
                "UPDATE portfolio SET shares = ?, total = ? WHERE id = ?",
                new_shares,
                new_total,
                portfolio_id,
            )
        else:
            # if no then insert a new entry
            db.execute(
                "INSERT INTO portfolio (user_id, symbol, name, shares, price, total) VALUES(?, ?, ?, ?, ? ,?)",
                session["user_id"],
                symbol,
                name,
                amount,
                price,
                total,
            )

        # insert the transaction into history
        db.execute(
            "INSERT INTO history (user_id, symbol, shares, price) VALUES(?, ?, ?, ?)",
            session["user_id"],
            symbol,
            amount,
            price,
        )

        # update the cash the user has
        new_cash = cash - total

        db.execute(
            "UPDATE users SET cash = ? WHERE id =?", new_cash, session["user_id"]
        )

        flash("Stock bought!")
        return redirect("/")

    return render_template("buy.html")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    history = db.execute("SELECT * FROM history WHERE user_id = ?", session["user_id"])

    # check theres a history
    if len(history) == 0:
        return apology("No history")

    return render_template("history.html", history=history)


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
            rows[0]["hash"], request.form.get("password")
        ):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/search", methods=["GET", "POST"])
@login_required
def search():
    """Search."""
    if request.method == "POST":
        # stock = lookup(request.form.get("symbol"))

        # if not stock:
        #     return apology("Stock doesn't exist")

        # name = stock["name"]
        # price = stock["price"]
        # symbol = stock["symbol"]
        return render_template("searchResult.html", name=name, price=price, symbol=symbol)

    return render_template("search.html")


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
            "INSERT INTO users (username, hash) VALUES(?, ?)",
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


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    owned_stock = db.execute(
        "SELECT symbol FROM portfolio WHERE user_id = ?", session["user_id"]
    )

    if request.method == "POST":
        symbol = request.form.get("symbol")
        amount = int(request.form.get("shares"))

        stock = db.execute(
            "SELECT * FROM portfolio WHERE symbol = ? AND user_id =?",
            symbol,
            session["user_id"],
        )

        shares = stock[0]["shares"]
        portfolio_id = stock[0]["id"]

        if amount > shares or amount < 0:
            return apology("You don't have that many shares")

        check = lookup(symbol)

        price = check["price"]

        # update cash in user account
        user = db.execute("SELECT * FROM users WHERE id = ?", session["user_id"])

        cash = user[0]["cash"]

        new_cash = cash + (price * amount)

        db.execute(
            "UPDATE users SET cash = ? WHERE id =?", new_cash, session["user_id"]
        )

        # remove amount of shares from portfolio and recalculate total
        new_shares = shares - amount

        if new_shares == 0:
            db.execute("DELETE FROM portfolio WHERE id = ?", portfolio_id)
        else:
            db.execute(
                "UPDATE portfolio SET shares = ? WHERE id = ?", new_shares, portfolio_id
            )

        # add to history
        db.execute(
            "INSERT INTO history (user_id, symbol, shares, price) VALUES(?, ?, ?, ?)",
            session["user_id"],
            symbol,
            -amount,
            price,
        )

        flash("Stock sold!")
        return redirect("/")

    return render_template("sell.html", owned_stock=owned_stock)


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
        if not check_password_hash(rows[0]["hash"], password):
            return apology("invalid password", 403)

        # update hash with new hash (new password)
        db.execute(
            "UPDATE users SET hash = ? WHERE id = ?",
            generate_password_hash(new_password, method="pbkdf2"),
            session["user_id"],
        )

        # Redirect user to home page
        flash("Password Changed!")
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("changePassword.html")
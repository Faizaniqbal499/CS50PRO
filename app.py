import os
from io import StringIO
import csv
from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, Response
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required

import datetime


# Configure application
app = Flask(__name__)


# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///students.db")


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
    # First check the user session
    user_id = session["user_id"]

    # Now get the data from contacts table for this user
    student_db = db.execute(
        "SELECT * FROM contacts WHERE user_id = ?",
        user_id,
    )

    # redirect to index page
    return render_template("index.html", database=student_db)



@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "GET":
        return render_template("register.html")

    else:
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

    # if no intup is entered
    if not username:
        return apology("Must provide a username")

    if not password:
        return apology("Must provide a password")

    if not confirmation:
        return apology("Must provide a confirmation")

    # Password comfirmation
    if password != confirmation:
        return apology("Password does not match")

    # Create hash(a secrect text) for password, as told in the instructions

    hash = generate_password_hash(password)

    # Inserting the data to our user table
    try:
        new_user = db.execute(
            "INSERT INTO users (username, hash) VALUES(?, ?)", username, hash
        )
    except:
        return apology("Username already exists")

    # start session and redirect to main page
    session["user_id"] = new_user
    return redirect("/")


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


@app.route("/add", methods=["GET", "POST"])
@login_required
def add():
    if request.method == "POST":
        name = request.form.get("name")
        city = request.form.get("city")
        number = request.form.get("number")

        if not name:
            return apology("Must provide a name")
        if not city:
            return apology("Must provide a city")
        elif not number:
            return apology("Must provide a number")

        user_id = session["user_id"]


        db.execute(
            "INSERT INTO contacts (user_id, name, city, number) VALUES(?, ?, ?, ?)",
            user_id,
            name,
            city,
            number,
        )

        flash("Record successfully added to database")

        return redirect("/")

    else:
        return render_template("add.html")



@app.route("/edit", methods=["GET", "POST"])
@login_required
def edit():
    if request.method == "POST":
        contact_id = request.form.get("id")
        name = request.form.get("name")
        city = request.form.get("city")
        number = request.form.get("number")

        if not name:
            # flash("Must provide a name")
            return redirect("/edit?id=" + contact_id)

        if not city:
            # flash("Must provide a city")
            return redirect("/edit?id=" + contact_id)

        if not number:
            # flash("Must provide a number")
            return redirect("/edit?id=" + contact_id)

        db.execute("UPDATE contacts SET name=?, city=?, number=? WHERE id=?",
                   name, city, number, contact_id)

        flash("Record successfully updated to the database")
        return redirect("/")

    else:
        contact_id = request.args.get('id')
        contact = db.execute("SELECT * FROM contacts WHERE id=?", contact_id)

        if contact:
            return render_template("edit.html", database=contact)

    flash("Contact not found")
    return redirect("/")


@app.route("/delete", methods=["POST"])
@login_required
def delete():
    contact_id = request.form.get("id")

    # Check if the contact_id exists
    existing_contact = db.execute("SELECT * FROM contacts WHERE id=?", contact_id)

    if existing_contact:
        # Delete the contact with the specified contact_id
        db.execute("DELETE FROM contacts WHERE id=?", contact_id)

        flash("Record successfully deleted from the database")
    else:
        flash("Contact not found")

    return redirect("/")


@app.route("/export", methods=["POST"])
@login_required
def export_csv():
    # Fetch all contacts with the specified 'user_id' from the session
    user_id = session["user_id"]
    contacts = db.execute("SELECT * FROM contacts WHERE user_id = ?", user_id)

    if contacts:
        # Create a CSV file in memory
        csv_data = StringIO()
        csv_writer = csv.writer(csv_data)

        # Write header row
        csv_writer.writerow(contacts[0].keys())

        # Write data rows
        for contact in contacts:
            csv_writer.writerow(contact.values())

        # Send the CSV file as a response to the user
        return Response(
            csv_data.getvalue(),
            mimetype="text/csv",
            headers={"Content-disposition": "attachment; filename=exported_data.csv"}
        )
    else:
        flash("No contacts found for the specified user_id")
        return redirect("/")

from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3
from pathlib import Path

app = Flask(__name__)
app.secret_key = "change-this-secret-key-before-deployment"
DATABASE = Path(__file__).with_name("food_rescue.db")


def get_db_connection():
    connection = sqlite3.connect(DATABASE)
    connection.row_factory = sqlite3.Row
    return connection


def init_db():
    connection = get_db_connection()
    connection.execute("""
        CREATE TABLE IF NOT EXISTS donations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            donor_name TEXT NOT NULL,
            food_name TEXT NOT NULL,
            quantity TEXT NOT NULL,
            location TEXT NOT NULL,
            contact TEXT NOT NULL,
            expiry_time TEXT NOT NULL,
            description TEXT
        )
    """)
    connection.execute("""
        CREATE TABLE IF NOT EXISTS food_requests (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            donation_id INTEGER NOT NULL,
            requester_name TEXT NOT NULL,
            contact TEXT NOT NULL,
            message TEXT,
            FOREIGN KEY (donation_id) REFERENCES donations (id)
        )
    """)
    connection.commit()
    connection.close()


@app.route("/")
def home():
    connection = get_db_connection()
    donation_count = connection.execute(
        "SELECT COUNT(*) FROM donations"
    ).fetchone()[0]
    connection.close()
    return render_template("index.html", donation_count=donation_count)


@app.route("/donate", methods=["GET", "POST"])
def donate():
    if request.method == "POST":
        donor_name = request.form.get("donor_name", "").strip()
        food_name = request.form.get("food_name", "").strip()
        quantity = request.form.get("quantity", "").strip()
        location = request.form.get("location", "").strip()
        contact = request.form.get("contact", "").strip()
        expiry_time = request.form.get("expiry_time", "").strip()
        description = request.form.get("description", "").strip()

        if not all([donor_name, food_name, quantity, location, contact, expiry_time]):
            flash("Please fill in all required fields.", "error")
            return render_template("donate.html")

        connection = get_db_connection()
        connection.execute("""
            INSERT INTO donations
            (donor_name, food_name, quantity, location, contact, expiry_time, description)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (donor_name, food_name, quantity, location, contact, expiry_time, description))
        connection.commit()
        connection.close()

        flash("Thank you! Your food donation has been added.", "success")
        return redirect(url_for("donations"))

    return render_template("donate.html")


@app.route("/donations")
def donations():
    connection = get_db_connection()
    all_donations = connection.execute(
        "SELECT * FROM donations ORDER BY id DESC"
    ).fetchall()
    connection.close()
    return render_template("donations.html", donations=all_donations)


@app.route("/request/<int:donation_id>", methods=["GET", "POST"])
def request_food(donation_id):
    connection = get_db_connection()
    donation = connection.execute(
        "SELECT * FROM donations WHERE id = ?", (donation_id,)
    ).fetchone()

    if donation is None:
        connection.close()
        flash("That donation could not be found.", "error")
        return redirect(url_for("donations"))

    if request.method == "POST":
        requester_name = request.form.get("requester_name", "").strip()
        contact = request.form.get("contact", "").strip()
        message = request.form.get("message", "").strip()

        if not requester_name or not contact:
            flash("Please enter your name and contact details.", "error")
            connection.close()
            return render_template("request.html", donation=donation)

        connection.execute("""
            INSERT INTO food_requests (donation_id, requester_name, contact, message)
            VALUES (?, ?, ?, ?)
        """, (donation_id, requester_name, contact, message))
        connection.commit()
        connection.close()
        flash("Your request has been submitted. The donor can contact you.", "success")
        return redirect(url_for("donations"))

    connection.close()
    return render_template("request.html", donation=donation)


@app.route("/about")
def about():
    return render_template("about.html")


init_db()

if __name__ == "__main__":
    app.run(debug=True)
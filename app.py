rom flask import Flask, render_template, request, jsonify, redirect, url_for
import sqlite3
import os
from datetime import datetime, date

app = Flask(__name__)
DB_PATH = "bookings.db"

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS bookings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            phone TEXT NOT NULL,
            date TEXT NOT NULL,
            time TEXT NOT NULL,
            guests INTEGER NOT NULL,
            table_no INTEGER NOT NULL,
            special_request TEXT,
            created_at TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

TABLES = [
    {"id": 1, "name": "Table 1", "capacity": 2, "location": "Window"},
    {"id": 2, "name": "Table 2", "capacity": 2, "location": "Window"},
    {"id": 3, "name": "Table 3", "capacity": 4, "location": "Main Hall"},
    {"id": 4, "name": "Table 4", "capacity": 4, "location": "Main Hall"},
    {"id": 5, "name": "Table 5", "capacity": 4, "location": "Main Hall"},
    {"id": 6, "name": "Table 6", "capacity": 6, "location": "Private Corner"},
    {"id": 7, "name": "Table 7", "capacity": 6, "location": "Private Corner"},
    {"id": 8, "name": "Table 8", "capacity": 8, "location": "Banquet Hall"},
]

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/book", methods=["GET", "POST"])
def book():
    if request.method == "POST":
        data = request.form
        name = data.get("name", "").strip()
        email = data.get("email", "").strip()
        phone = data.get("phone", "").strip()
        date_str = data.get("date", "").strip()
        time_str = data.get("time", "").strip()
        guests = int(data.get("guests", 1))
        table_no = int(data.get("table_no", 1))
        special_request = data.get("special_request", "").strip()

        if not all([name, email, phone, date_str, time_str]):
            return render_template("book.html", tables=TABLES, error="Please fill all required fields.")

        conn = get_db()
        c = conn.cursor()
        c.execute(
            "SELECT id FROM bookings WHERE date=? AND time=? AND table_no=?",
            (date_str, time_str, table_no)
        )
        existing = c.fetchone()
        if existing:
            conn.close()
            return render_template("book.html", tables=TABLES, error="That table is already booked at the selected date and time. Please choose another.")

        c.execute(
            """INSERT INTO bookings (name, email, phone, date, time, guests, table_no, special_request, created_at)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            (name, email, phone, date_str, time_str, guests, table_no, special_request, datetime.now().isoformat())
        )
        conn.commit()
        booking_id = c.lastrowid
        conn.close()
        return redirect(url_for("confirmation", booking_id=booking_id))

    return render_template("book.html", tables=TABLES)

@app.route("/confirmation/<int:booking_id>")
def confirmation(booking_id):
    conn = get_db()
    booking = conn.execute("SELECT * FROM bookings WHERE id=?", (booking_id,)).fetchone()
    conn.close()
    if not booking:
        return redirect(url_for("index"))
    table = next((t for t in TABLES if t["id"] == booking["table_no"]), None)
    return render_template("confirmation.html", booking=booking, table=table)

@app.route("/admin")
def admin():
    conn = get_db()
    bookings = conn.execute("SELECT * FROM bookings ORDER BY date DESC, time DESC").fetchall()
    conn.close()
    return render_template("admin.html", bookings=bookings, tables=TABLES)

@app.route("/admin/cancel/<int:booking_id>", methods=["POST"])
def cancel_booking(booking_id):
    conn = get_db()
    conn.execute("DELETE FROM bookings WHERE id=?", (booking_id,))
    conn.commit()
    conn.close()
    return redirect(url_for("admin"))

@app.route("/api/availability")
def availability():
    date_str = request.args.get("date")
    time_str = request.args.get("time")
    if not date_str or not time_str:
        return jsonify({"error": "date and time required"}), 400
    conn = get_db()
    booked = conn.execute(
        "SELECT table_no FROM bookings WHERE date=? AND time=?", (date_str, time_str)
    ).fetchall()
    conn.close()
    booked_ids = [row["table_no"] for row in booked]
    available = [t for t in TABLES if t["id"] not in booked_ids]
    return jsonify({"available_tables": available, "booked_table_ids": booked_ids})

if __name__ == "__main__":
    init_db()
    app.run(debug=True, port=5000)

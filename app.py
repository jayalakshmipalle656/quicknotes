from flask import Flask, render_template, request
import sqlite3
from datetime import datetime

app = Flask(__name__)

# Create database
conn = sqlite3.connect("notes.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS notes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    note TEXT,
    date TEXT
)
""")

conn.commit()
conn.close()


@app.route("/", methods=["GET", "POST"])
def home():

    if request.method == "POST":

        user_note = request.form["note"]
        current_date = datetime.now().strftime("%d-%m-%Y %H:%M")

        conn = sqlite3.connect("notes.db")
        cursor = conn.cursor()

        cursor.execute(
            "INSERT INTO notes(note, date) VALUES (?, ?)",
            (user_note, current_date)
        )

        conn.commit()
        conn.close()

    conn = sqlite3.connect("notes.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM notes ORDER BY id DESC")
    notes = cursor.fetchall()

    conn.close()

    return render_template(
        "index.html",
        notes=notes
    )


if __name__ == "__main__":
    app.run(debug=True)
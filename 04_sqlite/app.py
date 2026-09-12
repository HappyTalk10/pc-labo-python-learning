import sqlite3

from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)
DATABASE = "database.db"


def get_db():
    db = sqlite3.connect(DATABASE)
    db.row_factory = sqlite3.Row
    return db


def init_db():
    db = get_db()
    db.execute("""
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT NOT NULL,
            category TEXT NOT NULL,
            item TEXT NOT NULL,
            amount INTEGER NOT NULL
        )
    """)
    count = db.execute("SELECT COUNT(*) FROM expenses").fetchone()[0]
    if count == 0:
        db.executemany(
            "INSERT INTO expenses (date, category, item, amount) VALUES (?, ?, ?, ?)",
            [
                ("2026-08-01", "食費", "スーパー", 3200),
                ("2026-08-03", "交通費", "電車", 480),
                ("2026-08-05", "娯楽費", "映画", 1800),
            ],
        )
        db.commit()
    db.close()


@app.route("/")
def index():
    db = get_db()
    expenses = db.execute("SELECT * FROM expenses ORDER BY date").fetchall()
    db.close()
    return render_template("index.html", expenses=expenses)


@app.route("/add", methods=["POST"])
def add():
    db = get_db()
    db.execute(
        "INSERT INTO expenses (date, category, item, amount) VALUES (?, ?, ?, ?)",
        (
            request.form["date"],
            request.form["category"],
            request.form["item"],
            int(request.form["amount"]),
        ),
    )
    db.commit()
    db.close()
    return redirect(url_for("index"))


@app.route("/delete/<int:expense_id>", methods=["POST"])
def delete(expense_id):
    db = get_db()
    db.execute("DELETE FROM expenses WHERE id = ?", (expense_id,))
    db.commit()
    db.close()
    return redirect(url_for("index"))


init_db()

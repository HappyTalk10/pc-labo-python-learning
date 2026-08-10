from flask import Flask, render_template

app = Flask(__name__)

expenses = [
    {"date": "2026-08-01", "category": "食費", "item": "スーパー", "amount": 3200},
    {"date": "2026-08-03", "category": "交通費", "item": "電車", "amount": 480},
    {"date": "2026-08-05", "category": "娯楽費", "item": "映画", "amount": 1800},
]


@app.route("/")
def index():
    return render_template("index.html", expenses=expenses)

# 05_summary

「Pythonで学ぶ 家計簿アプリ開発」第5回のコード。

## app.py

```python
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
                ("2026-09-02", "食費", "スーパー", 4100),
                ("2026-09-10", "交通費", "電車", 480),
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


@app.route("/summary")
def summary():
    db = get_db()
    monthly = db.execute(
        "SELECT strftime('%Y-%m', date) AS month, SUM(amount) AS total "
        "FROM expenses GROUP BY month ORDER BY month"
    ).fetchall()
    by_category = db.execute(
        "SELECT category, SUM(amount) AS total "
        "FROM expenses GROUP BY category ORDER BY total DESC"
    ).fetchall()
    db.close()
    return render_template("summary.html", monthly=monthly, by_category=by_category)


init_db()
```

支出データを月別・カテゴリ別に集計し、グラフ（Chart.js）で表示する集計ページ（`/summary`）を追加する。あわせて、月をまたいだ集計を確認できるよう、初期データを5件（8月3件・9月2件）に増やしている。

## フォルダ構成

```
05_summary/
├── app.py
├── templates/
│   ├── index.html
│   └── summary.html
└── static/
    └── style.css
```

## 動かし方

```bash
cd 05_summary
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
flask --app app run --debug
```

すでに前回までの`database.db`がある場合は、初期データが増えないことがある（`init_db()`はデータが0件のときしか初期データを入れない仕様のため）。その場合は`database.db`を一旦削除してから起動すると、新しい初期データが入る。

Codespacesの場合、ポート転送のポップアップから「ブラウザで開く」を選ぶとアクセスできる。トップページの「集計を見る」リンクから`/summary`にアクセスできる。

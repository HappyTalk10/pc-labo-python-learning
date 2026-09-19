# 06_deploy-render

「Pythonで学ぶ 家計簿アプリ開発」第6回のコード。

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

アプリ本体は第5回と同じ。今回は、これをRenderにデプロイするための`requirements.txt`（gunicornを追加）と`Procfile`を用意する。

## フォルダ構成

```
06_deploy-render/
├── app.py
├── Procfile
├── requirements.txt
├── templates/
│   ├── index.html
│   └── summary.html
└── static/
    └── style.css
```

## Procfile

```
web: gunicorn --bind 0.0.0.0:$PORT app:app
```

Renderがこのコマンドでアプリを起動する。`$PORT`はRenderが自動的に割り当てる環境変数で、コード側で用意する必要はない。

## ローカルでの動かし方

```bash
cd 06_deploy-render
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
flask --app app run --debug
```

## Renderへのデプロイ手順

### 1. Renderのアカウントを作成する

1. [Render公式サイト](https://render.com/)にアクセスし、「Start for free」を選ぶ
2. 「Create an account」画面で、GitHub・GitLab・Bitbucket・Googleのアイコンから「GitHub」を選ぶ
3. GitHub側の認証画面で「Authorize Render」を押して連携を許可する
4. 認証が完了すると「Create a new Service」画面に進む

### 2. 新しいWebサービスを作成する

1. 「Create a new Service」画面で、「Web Services」カードの「New Web Service」を選ぶ
2. 「No repositories found」と表示された場合、「GitHub」ボタンから「Install Render」画面へ進む
3. インストール先のGitHubアカウントを選ぶ（複数ある場合は、ブログ用アカウントを選ぶ）
4. 「Install & Request Render」画面で「Only select repositories」を選び、`pc-labo-python-learning`を指定して「Install & Request」を押す
5. Renderの画面に戻り、リポジトリの一覧から`pc-labo-python-learning`を選んで「Connect」を押す

### 3. サービスの設定を入力する

| 項目 | 値 |
|---|---|
| Name | 好きなサービス名（例：`pc-labo-kakeibo`） |
| Root Directory | `06_deploy-render` |
| Runtime | Python 3 |
| Build Command | `pip install -r requirements.txt` |
| Start Command | `gunicorn --bind 0.0.0.0:$PORT app:app` |
| Instance Type | Free |

### 4. デプロイする

「Deploy web service」を押すと、ビルドとデプロイが自動的に始まる。完了すると`https://（サービス名）.onrender.com`のようなURLが発行される。

※ 無料プランはファイルシステムが永続化されないため、`database.db`の内容は再デプロイ・再起動のたびに初期状態に戻る。また、一定時間アクセスが無いとスリープし、次回アクセス時に起動し直すため、初回表示に時間がかかることがある。
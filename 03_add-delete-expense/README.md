# 03_add-delete-expense

「Pythonで学ぶ 家計簿アプリ開発」第3回のコード。

## app.py

```python
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

expenses = [
    {"date": "2026-08-01", "category": "食費", "item": "スーパー", "amount": 3200},
    {"date": "2026-08-03", "category": "交通費", "item": "電車", "amount": 480},
    {"date": "2026-08-05", "category": "娯楽費", "item": "映画", "amount": 1800},
]


@app.route("/")
def index():
    return render_template("index.html", expenses=expenses)


@app.route("/add", methods=["POST"])
def add():
    expenses.append({
        "date": request.form["date"],
        "category": request.form["category"],
        "item": request.form["item"],
        "amount": int(request.form["amount"]),
    })
    return redirect(url_for("index"))


@app.route("/delete/<int:index>", methods=["POST"])
def delete(index):
    expenses.pop(index)
    return redirect(url_for("index"))
```

支出データを、HTMLフォームから追加・削除できるようにする。まだデータベースは使っておらず、Pythonのリストにデータを持たせているだけなので、アプリを再起動すると初期状態のデータに戻る。

## フォルダ構成

```
03_add-delete-expense/
├── app.py
├── templates/
│   └── index.html
└── static/
    └── style.css
```

## 動かし方

```bash
cd 03_add-delete-expense
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
flask --app app run --debug
```

Codespacesの場合、ポート転送のポップアップから「ブラウザで開く」を選ぶとアクセスできる。

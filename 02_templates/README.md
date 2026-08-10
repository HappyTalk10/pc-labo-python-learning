# 02_templates

「Pythonで学ぶ 家計簿アプリ開発」第2回のコード。
## app.py
```python
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
```


固定の支出データを、Jinja2テンプレートを使って一覧表示する。

## フォルダ構成
```
02_templates/
├── app.py
├── templates/
│   └── index.html
└── static/
    └── style.css
```

## 動かし方

```bash
cd 02_templates
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
flask --app app run --debug
```

Codespacesの場合、ポート転送のポップアップから「ブラウザで開く」を選ぶとアクセスできる。

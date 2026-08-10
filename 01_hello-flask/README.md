# 01_hello-flask

「Pythonで学ぶ 家計簿アプリ開発」第1回のコード。

## app.py

```python
from flask import Flask

app = Flask(__name__)


@app.route("/")
def index():
    return "Hello, PC-LABO!"
```

Flaskの最小構成で、ブラウザに「Hello, PC-LABO!」を表示するだけのアプリ。

## フォルダ構成

```
01_hello-flask/
└── app.py
```

## 動かし方

```bash
cd 01_hello-flask
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
flask --app app run --debug
```

Codespacesの場合、ポート転送のポップアップから「ブラウザで開く」を選ぶとアクセスできる。
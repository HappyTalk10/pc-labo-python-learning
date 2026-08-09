# 01_hello-flask

「Pythonで学ぶ 家計簿アプリ開発」第1回のコード。

Flaskの最小構成で、ブラウザに「Hello, PC-LABO!」を表示するだけのアプリ。

## 動かし方

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
flask --app app run --debug
```

Codespacesの場合、ポート転送のポップアップから「ブラウザで開く」を選ぶとアクセスできる。

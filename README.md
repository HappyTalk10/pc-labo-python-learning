# pc-labo-python-learning

ブログ「[PC-LABO](https://pc-labo.online/)」の連載「Pythonで学ぶ 家計簿アプリ開発」で使用するコード置き場。

Python（Flask）を使い、家計簿アプリを1回ごとに1機能ずつ作りながら、Webアプリのバックエンド開発の基礎を学ぶ連載である。

## 連載の構成

| 回 | フォルダ | 内容 | 記事 |
|---|---|---|---|
| 第1回 | [`01_hello-flask`](./01_hello-flask) | Flask環境構築とHello Flask | 公開 |
| 第2回 | [`02_templates`](./02_templates) | Jinja2テンプレートで支出一覧を表示する | 公開  |
| 第3回 | `03_add-delete-expense` | フォームによる支出の追加・削除 | 準備中 |
| 第4回 | `04_sqlite` | SQLiteによるデータ永続化 | 準備中 |
| 第5回 | `05_summary` | 月別集計・グラフ表示 | 準備中 |
| 第6回 | `06_deploy-render` | Renderへのデプロイ | 準備中 |

## 技術スタック

- Python 3
- Flask
- SQLite（第4回以降）
- Render（第6回、デプロイ先）

## 使い方

各回のフォルダに、その回専用の`README.md`と`requirements.txt`を用意している。動かし方は各フォルダのREADMEを参照。

## 関連

- ブログ「PC-LABO」：<https://pc-labo.online/>
- カテゴリ「GitHubでつくって学ぶ」：<https://pc-labo.online/category/learn-by-building-on-github/>
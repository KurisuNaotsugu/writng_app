# Writing Practice Flask App

## 概要

このアプリは、TOEIC S&W や TOEFL のライティングセクションに沿った回答練習環境を提供する Flask アプリです。  
ユーザーはテストとタスクを選択し、回答を入力すると **AI（Gemini）** が添削・フィードバックを返します。  
さらに、タイマー機能と単語数カウントがあり、実践的な学習をサポートします。

---

## 主な機能

- テスト種別（TOEIC S&W、TOEFL）とタスク種別の選択  
- 選択に応じたタスクの指示（Direction）の表示と回答時間(タイマー)の設定  
- タイマー機能（Start / Pause）  
- 入力中の単語数カウント  
- 回答の送信と Gemini API によるフィードバック表示  
- JSON形式でのスコア・文法添削・改善例・解説・コメントの取得  

---

## 依存関係

- Python 3.10 以上  
- Flask  
- Bootstrap 5（CDN 使用）  
- **Gemini API（AI フィードバック用）**  

必要に応じて以下のパッケージをインストールしてください：

```bash
pip install flask
```

## Gemini API 設定
1. Gemini API に登録して APIキー を取得
2. 環境変数 GEMINI_API_KEY に設定

``` bash
# macOS / Linux
export GEMINI_API_KEY="your_api_key_here"

# Windows (PowerShell)
setx GEMINI_API_KEY "your_api_key_here"
```

3. アプリ起動時に app.py 内で Gemini API クライアントを自動的に初期化します。**API を呼ぶ部分のコードは不要です。**

## ディレクトリ構成
```
writing_app/
├── app/
│   ├── __init__.py
│   ├── writing/
│   │   ├── __init__.py
│   │   ├── routes.py
│   │   ├── templates/
│   │   │   └── writing_form.html
│   │   └── static/
│   │       ├── script.js
│   │       └── exam_data.json
├── run.py
└── README.md
```

## セットアップ
1. リポジトリをクローン
```bash
git clone <repo-url>
cd writing_app
```

2. 仮想環境を作成して有効化
```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

3. 依存パッケージをインストール
```bash
pip install flask
```

4. Gemini API キーを環境変数に設定（上記参照）
``` bash
static/exam_data.json にテスト・タスク情報を設定
```

例：
```
{
  "TOEIC": {
    "Writing": [
      {
        "task": "Email Response",
        "direction": "Write an email reply following the instructions.",
        "time_per_question_seconds": 600
      }
    ]
  },
  "TOEFL": {
    "Writing": [
      {
        "task": "Integrated Essay",
        "direction": "Summarize the reading and lecture in your own words.",
        "time_per_question_seconds": 900
      }
    ]
  }
}
```

6. Flask アプリを起動
```bash
export FLASK_APP=run.py  # Windows: set FLASK_APP=run.py
export FLASK_ENV=development
flask run
```

ブラウザで http://127.0.0.1:5000/writing/ にアクセス。

## 使い方

1. `Test` ドロップダウンでテストを選択
2. `Task` ドロップダウンでタスクを選択（選択後に Direction が表示されます）
3. 回答をテキストエリアに入力
4. Start / Pause でタイマーを管理
5. Submit を押すと Gemini API がフィードバックを返します

## 注意事項
- AI フィードバックは参考用であり、必ずしも正確ではありません
- タイマーや単語数は学習サポートのための目安です
- Gemini API の使用には通信料や利用制限が発生する場合があります

## カスタマイズ
- 新しいテストやタスクを exam_data.json に追加可能
- フロントエンドのデザインは writing_form.html と script.js で変更可能
- Gemini API 以外の AI に置き換えることも可能

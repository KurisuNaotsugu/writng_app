
# ✏️ English Learning App — Writing & Speaking Practice

このアプリは、Flask で構築された英語学習支援アプリです。
ユーザーは ライティング と スピーキング の練習を行い、AIによる自動フィードバックを受けることができます。

## 🌐 公開先:
🎯 アプリ本体（Render）:

👉 https://english-writng-app.onrender.com

📝 開発・技術解説ブログ（はてなブログ）:

👉 https://blog.hatena.ne.jp/Naotsugublog/naotsuguenglishblog.hatenablog.com/edit?entry=17179246901312617212

## 🚀 主な機能
### 🗣️ スピーキング練習

- 音声を録音し、OpenAI Whisper によって自動で文字起こし
- 文字起こし結果を Gemini API に送信してAIフィードバックを生成
- 発音・文法・内容などに関するフィードバックを表示

### ✍️ ライティング練習

- 英作文を入力・送信し、Gemini API により内容を評価
- 文法・語彙・構成に関する改善提案を自動生成

### 📄 レポート出力

- AIフィードバックを PDF形式（WeasyPrint使用） でダウンロード可能
- Writing / Speaking それぞれのレポートを生成

## 使用方法
1. テスト形式選択
- Home画面でテスト形式 (「TOEIC S&W」または「TOEFL」)と、練習するセクション (「Speaking」または「Writing」)を選択して、`Start Practice`ボタンを押してください
2. セクションに応じた練習ページに遷移
    1. Writingセクションの場合
    - 練習するタスク (問題番号)　を選択
    - 選択したタスクに対応したタイマーが自動でセットされます
    - `Start`ボタンを押すとタイマーがスタートするので、回答を初めてください
    - `Pause`ボタンで、タイマーを一時停止することもできます
    - 回答が完了したら`Submit`ボタンを押して回答を提出してください
    - Geminiからのフィードバックページに遷移します

    2. Speakingセクションの場合
    - 練習するタスク (問題番号)　を選択
    - 選択したタスクに対応したタイマーが自動でセットされます
    - `Record`ボタンを押すとタイマーと録音ががスタートします
    - `Stop`ボタンで、録音を停止します
    - `Transcribe`ボタンで、録音を文字起こししたものが表示されます
    - 文字起こしがうまくいっていない箇所があれば、手動で修正もできます
    - 回答が完了したら`Submit`ボタンを押して回答を提出してください
    - Geminiからのフィードバックページに遷移します

3. Geminiからのフィードバック
  - Geminiからのフィードバックを受けられます
  - 10点満点のスコアは採点基準不明なので、真に受けないように注意してください
  - 必要に応じて`Download PDF`から、レポートをダウンロードしてください

## 🧠 技術スタック
|カテゴリ|	使用技術|
|-|-|
|フレームワーク|	Flask (v3.1.2)|
|音声認識|	OpenAI Whisper|
|AI評価|	Google Gemini API|
|PDF生成|	WeasyPrint|
|サーバー|	Gunicorn（Procfile設定）|
|デプロイ|	Render|
|パッケージ管理|	Poetry|

## 📂 ディレクトリ構成
```
.
├── app.py                     # Flaskアプリのエントリポイント
├── common/
│   └── utils.py               # 共通関数
├── main/
│   ├── routes.py              # メインページのルート
│   ├── templates/main.html
│   └── static/main.js
├── writing/
│   ├── routes.py              # ライティング機能
│   ├── templates/writing_form.html
│   └── static/writing.js
├── report/
│   ├── routes.py              # フィードバック・PDF出力
│   ├── templates/
│   │   ├── feedback.html
│   │   ├── speaking_report.html
│   │   └── writing_report.html
├── templates/base.html        # ベーステンプレート
├── static/exam_data.json      # 問題データ等
├── Procfile                   # Render / Gunicorn 用設定
├── poetry.lock
├── pyproject.toml             # Poetry依存関係設定
└── README.md
```

## ⚙️ ローカル開発環境のセットアップ
### 1️⃣ 依存関係のインストール
```bash
poetry install
```
### 2️⃣ アプリの起動
```bash
poetry run flask --app app run
```

### 3️⃣ アクセス
```
http://localhost:5000
```

### 🔐 環境変数設定

.env または Render の「Environment Variables」に以下を設定してください：

GOOGLE_API_KEY=<your_gemini_api_key>


Whisper はローカル実行のため、追加キーは不要です。

## 💬 今後の展望

- ローディングスピナー追加
- プロンプトの最適化
- ログイン認証機能、過去の回答の閲覧・保存
- スピーキング音声の保存・再生機能
- Geminiモデル選択機能（Pro / Flash対応）

## 👤 作者

Naotsugu Kurisu


## 🪄 ライセンス

このプロジェクトは MIT ライセンスのもとで公開されています。
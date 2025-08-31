from flask import render_template, request
from weasyprint import HTML
from . import writing_bp
import json
import re
import os

def count_words(text: str) -> int:
    """Count words in a given text."""
    words = text.strip().split()
    return 0 if not words or words[0] == "" else len(words)

@writing_bp.route('/', methods=['GET', 'POST'])
def writing():
    feedback = None
    user_text = ""
    test_type = ""
    task_type = ""
    time_limit = 15 * 60

    # jsonファイルを読み込み
    json_path = os.path.join('static', 'exam_data.json')
    with open(json_path, encoding='utf-8') as f:
        exam_data = json.load(f)

    if request.method == 'POST':
        user_text = request.form.get('user_text', '')
        test_type = request.form.get("test_type", '')
        task_type = request.form.get("task_type", '')

        # 選択されたタスクの制限時間を設定
        if test_type and task_type:
            tasks = exam_data[test_type]["Writing"]
            task = next((t for t in tasks if t["task"] == task_type), None)
            if task:
                time_limit = task.get("time_per_question_seconds", time_limit)

        prompt = f"""
                あなたは英語試験の採点官です。
                以下の情報に基づき、受験者の英文を評価してください。

                【テストの種類】 : {test_type}
                【タスクの種類】 : {task_type}
                【受験者の回答】 : {user_text}

                評価基準:
                1. スコア （テストの種類に応じて）
                2. 文法・スペルミス
                3. 回答例（もとの例文を踏襲してより高得点が狙える文章に）
                4. 回答例の解説
                5. コメント（完結に、短く）

                出力形式は以下のJSON形式にして、それ以外に余分な情報は出力しないでください。:
                {{
                "score": 数値(10点満点),
                "grammar_and_spell_errors": ["エラー1", "エラー2"],
                "corrected_text": "添削後の英文",
                "improved_text": "より良い回答例",
                "explanation": "添削の解説",
                "feedback": "コメント"
                }}
                """

        if user_text and writing_bp.client:
            response = writing_bp.client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt,
            )
            raw_text = response.text.strip()    
            clean_text = re.sub(r"^```json|```$", '', raw_text, flags=re.DOTALL).strip()

            try:
                feedback = json.loads(clean_text)
            except json.JSONDecodeError:
                feedback = {"error": "JSON parse failed", "raw": raw_text}

        json_path = os.path.join('static','exam_data.json')
        with open(json_path, encoding='utf-8') as f:
            exam_data = json.load(f)

    return render_template('writing_form.html', 
                            feedback=feedback,
                            exam_data=exam_data,
                            user_text=user_text,
                            test_type=test_type,
                            task_type=task_type,
                            time_limit=time_limit
                            )

@writing_bp.route("/report", methods=["POST"])
def generate_report():
    # フォームのデータを受け取る
    user_text = request.form.get("user_text", "")
    test_type = request.form.get("test_type", "")
    task_type = request.form.get("task_type", "")
    feedback = request.form.get("feedback")

    # 単語数カウント
    word_count = count_words(user_text)

    # feedback が JSON 文字列なら辞書に変換
    try:
        feedback_dict = json.loads(feedback)
    except Exception:
        feedback_dict = {}

    # HTMLテンプレートでPDF内容を作成
    html = render_template(
        "writing_report.html",
        user_text=user_text,
        test_type=test_type,
        task_type=task_type,
        feedback=feedback_dict,
        word_count=word_count
    )

    # PDFに変換
    pdf = HTML(string=html).write_pdf()

    # PDFを返す
    response = make_response(pdf)
    response.headers["Content-Type"] = "application/pdf"
    response.headers["Content-Disposition"] = f"attachment; filename=report_{test_type}_{task_type}.pdf"
    return response
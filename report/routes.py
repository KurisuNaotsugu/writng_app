from flask import render_template, request, make_response, current_app
from weasyprint import HTML
import json
import re
import os
from common.utils import load_exam_data, count_words, get_gemini_response

from . import report_bp

@report_bp.route("/feedback", methods=["POST"])
def feedback():
    # 試験データと回答の取得
    skill_type = request.form.get('skill_type', '')
    test_type = request.form.get("test_type", '')
    task_type = request.form.get("task_type", '')
    user_text = request.form.get('user_text', '')

    prompt = f"""
            あなたは英語試験の採点官です。
            以下の情報に基づき、受験者の英文を評価してください。

            【テストの種類】 : {test_type}
            【スキルの種類】 : {skill_type}
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

    # GeminiAPIからの応答を取得
    client = current_app.config['GENAI_CLIENT']
    if user_text and client:
        feedback = get_gemini_response(client, prompt, model="gemini-2.5-flash")
    else:
        feedback = None

    return render_template('feedback.html', 
                            feedback=feedback,
                            user_text=user_text,
                            test_type=test_type,
                            skill_type=skill_type,
                            task_type=task_type,
                            )

@report_bp.route("/report", methods=["POST"])
def report():
    # データ取得
    test_type = request.form.get("test_type", "")
    skill_type = request.form.get("skill_type", "")
    task_type = request.form.get("task_type", "")
    user_text = request.form.get("user_text", "")
    feedback = request.form.get("feedback")

    word_count = count_words(user_text)
    feedback_dict = json.loads(feedback)

    # テンプレート選択
    if skill_type == "speaking":
        template_html = "speaking_report.html"
    else:
        template_html = "writing_report.html"

    # レポート作成
    html = render_template(
        template_html,
        user_text=user_text,
        test_type=test_type,
        task_type=task_type,
        feedback=feedback_dict,
        word_count=word_count
    )
    pdf = HTML(string=html).write_pdf()

    # PDFを返す
    response = make_response(pdf)
    response.headers["Content-Type"] = "application/pdf"
    response.headers["Content-Disposition"] = f"attachment; filename=report_{test_type}_{task_type}.pdf"
    return response
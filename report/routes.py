from flask import render_template, request, make_response
from weasyprint import HTML
import json
import re
import os
from common.utils import count_words

from . import report_bp

@report_bp.route("/report", methods=["POST"])
def generate_report():
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
        template_html = "report_speaking.html"
    else:
        template_html = "report_writing.html"

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
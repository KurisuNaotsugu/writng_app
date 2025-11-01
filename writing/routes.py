from flask import render_template, make_response, current_app, request
import json
import re
import os
import common.utils as ut
from . import writing_bp

@writing_bp.route('/create_form', methods=['POST'])
def create_form():
    # mainページからテスト形式とスキルタイプを取得
    test_type = request.form.get("test_type", '')
    skill_type = request.form.get("skill_type", '')

    # jsonファイルを読み込み
    json_path = os.path.join('static', 'exam_data.json')
    exam_data = ut.load_exam_data(json_path)

    # スキルタイプに応じて適切なフォームをレンダリング
    if skill_type == 'Writing':
        return render_template('writing_form.html',
                                exam_data=exam_data,
                                test_type=test_type,
                                skill_type=skill_type,
                                )
    else:
        return render_template('speaking_form.html',
                                exam_data=exam_data,
                                test_type=test_type,
                                skill_type=skill_type,
                                )
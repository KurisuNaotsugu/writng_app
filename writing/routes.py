from flask import render_template, make_response, current_app, request, jsonify
import json
import tempfile
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
    
@writing_bp.route('/transcript', methods=['POST'])
def transcript_audio():
    # mainページからテスト形式とスキルタイプを取得
    test_type = request.form.get("test_type", '')
    skill_type = request.form.get("skill_type", '')
    task_type = request.form.get("task_type", '')

    if 'audio_file' not in request.files:
        return jsonify({"error": "No audio file uploaded"}), 400

    audio_file = request.files['audio_file']

    # 一時ファイルに保存
    with tempfile.NamedTemporaryFile(delete=False, suffix=".webm") as tmp:
        audio_file.save(tmp.name)
        temp_path = tmp.name

    # Whisperで文字起こし
    transcript_text = ut.get_whisper_transcript(temp_path, model_size='base')

    # 一時ファイル削除
    os.remove(temp_path)

    # JSONで返す
    return jsonify({"transcript": transcript_text})
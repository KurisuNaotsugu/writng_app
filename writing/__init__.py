from flask import Blueprint

writing_bp = Blueprint(
    'writing', 
    __name__, 
    template_folder='../templates', 
    static_folder='../static',
    static_url_path='/static'
)

# app.py からセットされる Gemini API クライアント
writing_bp.client = None

# ルート関数を import して Blueprint に登録
from . import routes

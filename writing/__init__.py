from flask import Blueprint

# Blueprintインスタンス作成
writing_bp = Blueprint(
    'writing', 
    __name__, 
    template_folder='templates',
    static_folder='static'
)

# Gemini API クライアント登録用インスタンス 
writing_bp.client = None

# routes.pyを import して writing_bp にルート関数を登録
from . import routes
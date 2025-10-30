from flask import Blueprint

speaking_bp = Blueprint(
    'speaking', 
    __name__, 
    template_folder='templates', 
    static_folder='static',
)

# Gemini API クライアント登録用インスタンス 
speaking_bp.client = None

# routes.pyを import して speaking_bp にルート関数を登録
from . import routes

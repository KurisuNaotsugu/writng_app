from flask import Blueprint

# Blueprintインスタンス作成
main_bp = Blueprint(
    'main', 
    __name__, 
    template_folder='templates',
    static_folder='static'
)

# routes.pyを import して main_bp にルート関数を登録
from . import routes
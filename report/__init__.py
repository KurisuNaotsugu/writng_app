from flask import Blueprint

# Blueprintインスタンス作成
report_bp = Blueprint(
    'report', 
    __name__, 
    template_folder='templates',
    static_folder='static'
)

# routes.pyを import して report_bp にルート関数を登録
from . import routes
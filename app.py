import os
from flask import Flask
import google.genai as genai

# Import the Blueprint
from main import main_bp
from writing import writing_bp
from speaking import speaking_bp
from report import report_bp

def create_app():
    app = Flask(__name__)

    # Gemini API クライアント作成
    client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
    app.config['GENAI_CLIENT'] = client

    # Blueprint をアプリに登録
    app.register_blueprint(main_bp)
    app.register_blueprint(writing_bp, url_prefix='/writing')
    app.register_blueprint(speaking_bp, url_prefix='/speaking')
    app.register_blueprint(report_bp, url_prefix='/report')
    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)

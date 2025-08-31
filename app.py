import os
from flask import Flask
import google.genai as genai
from writing import writing_bp  # Blueprint

def create_app():
    app = Flask(__name__)

    # Gemini API クライアント作成
    client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
    print(f"Using Gemini API Key: {os.getenv('GEMINI_API_KEY')}")

    # Blueprint に client を渡す
    writing_bp.client = client
    app.register_blueprint(writing_bp, url_prefix='/writing')

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)

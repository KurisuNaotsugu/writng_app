import os
import re
import json

def count_words(text: str) -> int:
    """Count words in a given text."""
    words = text.strip().split()
    return 0 if not words or words[0] == "" else len(words)

def load_exam_data(json_path:str, encoding:str='utf-8') -> dict:
    """Load exam data from JSON file."""
    with open(json_path, encoding=encoding) as f:
        return json.load(f)
    
def get_gemini_response(bp, prompt: str, model: str="gemini-2.5-flash") -> dict:
    """Get response from Gemini API and parse JSON."""
    response = bp.client.models.generate_content(model=model, contents=prompt)
    raw_text = response.text.strip()    
    clean_text = re.sub(r"^```json|```$", '', raw_text, flags=re.DOTALL).strip()

    try:
        feedback = json.loads(clean_text)
    except json.JSONDecodeError:
        feedback = {"error": "JSON parse failed", "raw": raw_text}

    return feedback
import os
import re
import json
import whisper

def count_words(text: str) -> int:
    """Count words in a given text."""
    words = text.strip().split()
    return 0 if not words or words[0] == "" else len(words)

def load_exam_data(json_path:str, encoding:str='utf-8') -> dict:
    """Load exam data from JSON file."""
    with open(json_path, encoding=encoding) as f:
        return json.load(f)
    
def get_gemini_response(client, prompt: str, model: str="gemini-2.5-flash") -> dict:
    """Get response from Gemini API and parse JSON."""
    response = client.models.generate_content(model=model, contents=prompt)
    raw_text = response.text.strip()    
    clean_text = re.sub(r"^```json|```$", '', raw_text, flags=re.DOTALL).strip()

    try:
        feedback = json.loads(clean_text)
    except json.JSONDecodeError:
        feedback = {"error": "JSON parse failed", "raw": raw_text}

    return feedback

def get_whisper_transcript(audio_path: str, model_size: str='base') -> str:
    """Transcribe audio using Whisper model."""
    model = whisper.load_model(model_size)
    result = model.transcribe(audio_path,
                            language="en",
                            fp16=False)
    return result['text']
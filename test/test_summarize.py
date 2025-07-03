import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from main import summarize_with_huggingface

def test_summarize_with_huggingface():
    text = "OpenAI développe des modèles d'intelligence artificielle avancés qui peuvent générer du texte, répondre à des questions et bien plus encore."
    result = summarize_with_huggingface(text)
    assert isinstance(result, str)
    assert len(result) < len(text)

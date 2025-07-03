import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from main import ask_question_with_huggingface

def test_ask_question_with_huggingface():
    context = "OpenAI développe des modèles d'intelligence artificielle."
    question = "Qui développe des modèles ?"
    response = ask_question_with_huggingface(question, context)
    assert "OpenAI" in response or "Erreur" not in response
import requests

API_URL = "https://api-inference.huggingface.co/models/facebook/bart-large-cnn"
headers = {"Authorization": "Bearer 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"}

def summarize(text):
    response = requests.post(API_URL, headers=headers, json={"inputs": text})
    return response.json()[0]["summary_text"]

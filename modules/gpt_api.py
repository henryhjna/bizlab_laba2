import requests
import os
from dotenv import load_dotenv

def load_api_key():
    # .env 파일 로드
    load_dotenv(dotenv_path="config/.env")
    
    # 환경 변수에서 API 키 읽기
    api_key = os.getenv("API_KEY")
    if not api_key:
        raise ValueError("API_KEY is missing in config/.env")
    return api_key

def gptai(model_type, token_size, system_message, user_prompt, api_key):
    url = "https://api.openai.com/v1/chat/completions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}",
    }
    data = {
        "model": model_type,
        "messages": [
            {"role": "system", "content": system_message},
            {"role": "user", "content": user_prompt},
        ],
        "max_tokens": token_size,
        "temperature": 0.5,
        "top_p": 1,
        "frequency_penalty": 0,
        "presence_penalty": 0,
    }
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        return response.json()
    else:
        return {"error": response.status_code, "message": response.text}

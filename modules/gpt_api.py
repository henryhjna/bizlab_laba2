import requests

def load_api_key(file_path="config/api_key.txt"):
    with open(file_path, 'r') as f:
        return f.read().strip()

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

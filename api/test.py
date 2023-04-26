import openai
from config import default_config

if __name__ == '__main__':
    openai.api_key = default_config['api_key']
    dt = {
        "model": "gpt-3.5-turbo",
        "messages": [{'role': 'user', 'content': '你好'}],
        "temperature": 1,
        "max_tokens": 512
    }
    response = openai.ChatCompletion.create(**dt, timeout=60)
    print(response.choices[0].message.content)

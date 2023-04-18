import openai

if __name__ == '__main__':
    openai.api_key = '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 '
    dt = {
        "model": "gpt-3.5-turbo",
        "messages": [{'role': 'user', 'content': '你好'}],
        "temperature": 1,
        "max_tokens": 512
    }
    response = openai.ChatCompletion.create(**dt, timeout=60)
    print(response.choices[0].message.content)

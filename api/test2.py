import requests
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def talk_to_chatgpt():
    dt = {
        "model": "gpt-3.5-turbo-0613",
        "messages": [{"role": "user", "content": "写封邮件给123456789.com. 向他问好!"}],
        "functions": [{
            "name": "send_email",
            "description": "给指定的邮箱发邮件",
            "parameters": {
                "type": "object",
                "properties": {
                    "email": {"type": "string", "describtion": "目标邮箱地址"},
                    "body": {"type": "string"},
                    "subject": {"type": "string"}
                }
            }
        }],
        "temperature": 1,
        "max_tokens": 512
    }
    API_URL = 'https://8.219.97.149:8000/v1/chat/completions'
    message = {'role': 'assistant', 'content': ''}
    try:
        x = requests.post(API_URL, json=dt, verify=False)

        # 用自己的api key：
        # api_key='sk-......'
        # x = requests.post(API_URL, json=dt, headers={"Authorization": f"Bearer {api_key}"},verify=False)

        message = x.json()['choices'][0]['message']
    except Exception as e:
        message['content'] = str(e)
    finally:
        return message

print(talk_to_chatgpt())

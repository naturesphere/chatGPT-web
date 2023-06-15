import openai
from config import default_config


def case_openai_chat():
    openai.api_key = default_config['api_key']
    dt = {
        "model": "gpt-3.5-turbo",
        "messages": [{'role': 'user', 'content': '你好'}],
        "temperature": 1,
        "max_tokens": 512
    }
    response = openai.ChatCompletion.create(**dt, timeout=60)
    print(response.choices[0].message.content)


def case_openai_function_call():
    openai.api_key = default_config['api_key']
    dt = {
        "model": "gpt-3.5-turbo-0613",
        "messages": [{'role': 'user', 'content': 'Send an email to 123456789.com. Tell him to pay my money back!'}],
        "functions": [{
            'name': 'send_email',
            'description': 'Sends an email to the specified email address',
            'parameters': {
                'type': 'object',
                'properties': {
                    'email': {'type': 'string', 'describtion': 'An email address to send the email to'},
                    'body': {'type': 'string'},
                    'subject': {'type': 'string'}
                }
            }
        }],
        "temperature": 1,
        "max_tokens": 512
    }
    response = openai.ChatCompletion.create(**dt, timeout=60)
    print(response.choices[0].message.content)


if __name__ == '__main__':
    case_openai_chat()
    case_openai_function_call()

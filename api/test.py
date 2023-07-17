import openai
from app import get_api_key
import os

openai.api_key = get_api_key()


def case_openai_chat():
    dt = {
        "model": "gpt-3.5-turbo",
        "messages": [{'role': 'user', 'content': '你好'}],
        "temperature": 1,
        "max_tokens": 512
    }
    response = openai.ChatCompletion.create(**dt, timeout=60)
    print(response.choices[0].message)


def case_openai_function_call():
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
    print(response.choices[0].message)


if __name__ == '__main__':
    case_openai_chat()
    case_openai_function_call()

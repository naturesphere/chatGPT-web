import gradio as gr
import random
import requests
from openai import OpenAI
from fastapi import FastAPI, Request, Header
from typing import Union
import logging, os
from logging.handlers import RotatingFileHandler
import time

file_handler = RotatingFileHandler('log.txt', mode='a',
                                   maxBytes=1024 * 1024,
                                   backupCount=20, encoding='utf8')
file_handler.setLevel(logging.INFO)
file_handler.setFormatter(logging.Formatter('[%(asctime)s-%(filename)s-%(levelname)s:%(message)s]'))
logger = logging.getLogger(__file__)
logger.setLevel(logging.INFO)
logger.addHandler(file_handler)

API_KEY = os.environ.get('OPENAI_API_KEY')
logger.info(f'init api key:{API_KEY}')

Client_DT = {API_KEY: OpenAI(api_key=API_KEY)}

app = FastAPI()


def get_api_key(Authorization: str = None):
    bearer = 'Bearer'
    if Authorization:
        api_key = Authorization.split()[-1]
        if api_key.startswith(bearer):
            api_key = api_key[len(bearer):]
        if api_key.startswith('sk-'):
            return api_key
    return API_KEY


def get_massages(message, chat_history, max_turn=3):
    messages = []
    for user_text, bot_text in chat_history[-max_turn:]:
        messages.append({"role": "user", "content": user_text})
        messages.append({'role': 'assistant', 'content': bot_text})
    messages.append({"role": "user", "content": message})
    return messages


def talk_to_chatgpt(message, chat_history):
    max_turn = 3
    messages = get_massages(message, chat_history, max_turn)
    dt = {
        "model": "gpt-3.5-turbo",
        "messages": messages,
        "temperature": 1,
        "max_tokens": 512
    }
    client = Client_DT[API_KEY]
    try:
        response = client.chat.completions.create(**dt, timeout=60)
        message = response.choices[0].message.content
    except Exception as e:
        message = str(e)
    finally:
        return message


with gr.Blocks() as demo:
    chatbot = gr.Chatbot()
    msg = gr.Textbox()
    clear = gr.ClearButton([msg, chatbot])


    def respond(message, chat_history):
        max_history = 99
        bot_message = talk_to_chatgpt(message, chat_history)
        logger.info(f'chatbot=> user:{message}, bot:{bot_message}')
        chat_history.append((message, bot_message))
        if len(chat_history) > max_history:
            chat_history = chat_history[-max_history:]
        return "", chat_history


    msg.submit(respond, [msg, chatbot], [msg, chatbot])


# demo.launch(server_name='0.0.0.0', share=False, ssl_verify=False)


@app.post('/v1/chat/completions')
async def talk(request: Request, Authorization: Union[str, None] = Header(default=None)):
    api_key = get_api_key(Authorization)
    if api_key not in Client_DT:
        logger.info(f'Authorization: {Authorization}, request api_key: {api_key}')
        Client_DT[api_key] = OpenAI(api_key=api_key)
    client = Client_DT[api_key]
    response = 'ERROR!!!'
    try:
        parameters = await request.json()
        logger.info(f'parameters: {parameters}')
        tik = time.time()
        response = client.chat.completions.create(**parameters, timeout=60)
        tok = time.time()
        logger.info(f"elapsed: {tok - tik:.3f}s, 回复: {response}")
    except Exception as e:
        se = str(e)
        logger.exception('ERROR!!!')
        response = se
    finally:
        return response


if __name__ == '__main__':
    import uvicorn

    app = gr.mount_gradio_app(app, demo, path='/')
    uvicorn.run(app, host="0.0.0.0", port=7860)

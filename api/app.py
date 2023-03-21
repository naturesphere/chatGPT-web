import os
import openai
from fastapi import FastAPI, Request, Header
from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from typing import Union
from model import Message
import aiohttp, asyncio
import logging, os
from logging.handlers import RotatingFileHandler
import time

file_handler = RotatingFileHandler('log.txt', mode='a',
                                   maxBytes=1024 * 1024,
                                   backupCount=2, encoding='utf8')
file_handler.setLevel(logging.INFO)
file_handler.setFormatter(logging.Formatter('[%(asctime)s-%(filename)s-%(levelname)s:%(message)s]'))
logger = logging.getLogger(__file__)
logger.setLevel(logging.INFO)
logger.addHandler(file_handler)

API_KEY = os.environ.get('API_KEY')
logger.info(f'init api key:{API_KEY}')

app = FastAPI()


def get_api_key(Authorization: str = None):
    if Authorization:
        api_key = Authorization.split()[-1]
        if api_key.startswith('sk-'):
            return api_key
    return API_KEY


@app.post('/v1/chat/completions')
async def cc(message: Message, Authorization: Union[str, None] = Header(default=None)):
    api_key = get_api_key(Authorization)
    openai.api_key = api_key
    try:
        tik = time.time()
        response = await openai.ChatCompletion.acreate(**message.dict(), timeout=0.1)
        tok = time.time()
        logger.info(f'post api_key: {api_key}, elapsed: {tok-tik:.3f}s')
        return response
    except Exception as e:
        return str(e)


if __name__ == '__main__':
    import uvicorn

    uvicorn.run("app:app", host="0.0.0.0", port=8001, reload=True,
                ssl_keyfile='./key.pem', ssl_certfile='./cert.pem')

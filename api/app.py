import os
import openai
from fastapi import FastAPI, Request, Header
from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from typing import Union
from model import Message, get_parameters
import aiohttp, asyncio
import logging, os
from logging.handlers import RotatingFileHandler
import time
import httpx

file_handler = RotatingFileHandler('log.txt', mode='a',
                                   maxBytes=1024 * 1024,
                                   backupCount=20, encoding='utf8')
file_handler.setLevel(logging.INFO)
file_handler.setFormatter(logging.Formatter('[%(asctime)s-%(filename)s-%(levelname)s:%(message)s]'))
logger = logging.getLogger(__file__)
logger.setLevel(logging.INFO)
logger.addHandler(file_handler)

API_KEY = os.environ.get('API_KEY')
logger.info(f'init api key:{API_KEY}')

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


@app.post('/v1/chat/completions')
async def cc(message: Message, Authorization: Union[str, None] = Header(default=None)):
    api_key = get_api_key(Authorization)
    logger.info(f'Authorization: {Authorization}, request api_key: {api_key}')
    openai.api_key = api_key
    dt = dict()
    try:
        logger.info(f'message: {message}')
        tik = time.time()
        parameters = get_parameters(message)
        response = await openai.ChatCompletion.acreate(parameters, timeout=60)
        tok = time.time()
        dt = response.json()
        logger.info(f"elapsed: {tok - tik:.3f}s, 回复: {dt['choices'][0]['message']}")
    except Exception as e:
        se = str(e)
        logger.exception('error:')
        dt = {'error': se}
    finally:
        return dt


if __name__ == '__main__':
    import uvicorn

    uvicorn.run("app:app", host="0.0.0.0", port=8001, reload=True,
                ssl_keyfile='./key.pem', ssl_certfile='./cert.pem')

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
    if Authorization:
        api_key = Authorization.split()[-1]
        if api_key.startswith('sk-'):
            return api_key
    return API_KEY


@app.post('/v1/chat/completions')
async def cc(message: Message, Authorization: Union[str, None] = Header(default=None)):
    api_key = get_api_key(Authorization)
    openai.api_key = api_key
    logger.info(f'post api_key: {api_key}')
    logger.info(f'{message.messages}')
    dt = dict()
    try:
        tik = time.time()
        response = await openai.ChatCompletion.acreate(**message.dict(), timeout=60)
        tok = time.time()
        dt = response.json()
        logger.info(f"elapsed: {tok - tik:.3f}s, 回复: {dt['choices'][0]['message']}")
    except Exception as e:
        se = str(e)
        logger.error(se)
        dt = {'error': se}
    finally:
        return dt


@app.get('/dashboard/billing/credit_grants')
async def credit_summary(api_key=None):
    """Get the credit summary for the API key."""
    url = "https://api.openai.com/dashboard/billing/credit_grants"
    async with httpx.AsyncClient() as client:
        response = await client.get(
            url,
            headers={"Authorization": f"Bearer {api_key}"},
            timeout=60,
        )
        return response.json()


if __name__ == '__main__':
    import uvicorn

    uvicorn.run("app:app", host="0.0.0.0", port=8002, reload=True,
                ssl_keyfile='./key.pem', ssl_certfile='./cert.pem')

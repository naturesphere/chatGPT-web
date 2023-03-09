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

API_KEY = os.environ.get('API_KEY')
print(API_KEY)

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
        response = await openai.ChatCompletion.acreate(**message.dict(), timeout=30)
        return response
    except Exception as e:
        return str(e)


if __name__ == '__main__':
    import uvicorn

    uvicorn.run("app:app", host="0.0.0.0", port=8000)

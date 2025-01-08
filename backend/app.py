import requests
from fastapi import FastAPI, Response
from fastapi.responses import FileResponse
from src.generator import chat_main
import os

app = FastAPI()

@app.get('/')
def home():
    return {"Chat" : "Bot"}

# @app.get("/favicon.ico", include_in_schema=False)
# def favicon():
#     return FileResponse(os.path.join(os.path.dirname(__file__), 'favicon.ico'))
@app.get('/favicon.ico', include_in_schema=False)
async def favicon():
    favicon_path = os.path.join('static', 'favicon.ico')
    return FileResponse(favicon_path)

@app.get('/ask')
def ask(prompt :str):
    print('\n===================\n')
    print('prompt = ',prompt)
    print('\n===================\n')
    
    res = chat_main(prompt)
    print('\n===================\n')
    print('response = ',res)
    print('\n===================\n')

    return Response(content=res)
    
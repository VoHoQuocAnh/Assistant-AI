import os
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from app.routes import chat

app = FastAPI(title="Mini AI Chatbot API")
app.include_router(chat.router)
if os.path.exists("static"):
    app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/", response_class=HTMLResponse)
def home():
    if os.path.exists("static/giaodien.html"):
        with open("static/giaodien.html", "r", encoding="utf-8") as f:
            return f.read()

    return "<h1>Mini AI Chatbot API đang chạy. Vui lòng kiểm tra lại thư mục static/giaodien.html</h1>"
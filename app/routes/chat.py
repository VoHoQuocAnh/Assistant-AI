from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.services.ai_service import ask_ai

router = APIRouter()
chat_history = []

class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    response: str

@router.post("/chat", response_model=ChatResponse)
def chat_endpoint(request: ChatRequest):
    if not request.message.strip():
        raise HTTPException(status_code=400, detail="Tin nhắn không được để trống")
    
    ai_reply = ask_ai(request.message)
    
    chat_history.append({
        "user": request.message,
        "assistant": ai_reply
    })
    
    return ChatResponse(response=ai_reply)

@router.get("/history")
def get_history():
    return chat_history

@router.delete("/history")
def clear_history():
    chat_history.clear()
    return {"message": "Đã xóa toàn bộ lịch sử chat"}
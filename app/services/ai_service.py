import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=api_key) if api_key else None

# Biến bộ nhớ tạm dùng để lưu model chạy tốt nhất
WORKING_MODEL = None

def ask_ai(prompt: str) -> str:
    global WORKING_MODEL
    if not client:
        return "Lỗi: Chưa cấu hình GEMINI_API_KEY trong file .env"
    
    # ⚡ CÁCH SIÊU TỐC: Nếu đã tìm thấy model ngon từ trước, dùng thẳng luôn (0.1 giây)
    if WORKING_MODEL:
        try:
            response = client.models.generate_content(
                model=WORKING_MODEL,
                contents=prompt,
            )
            return response.text
        except Exception:
            WORKING_MODEL = None  # Reset nếu model gặp sự cố để dò lại
            
    # 🔍 DÒ TÌM MODEL KHẢ DỤNG (Chỉ chạy 1 LẦN DUY NHẤT ở câu hỏi đầu tiên)
    try:
        models = list(client.models.list())
        
        # Sắp xếp ưu tiên các model 'flash' để tốc độ phản hồi nhanh nhất
        flash_models = [m for m in models if "flash" in m.name.lower()]
        other_models = [m for m in models if "flash" not in m.name.lower()]
        sorted_models = flash_models + other_models

        for m in sorted_models:
            try:
                response = client.models.generate_content(
                    model=m.name,
                    contents=prompt,
                )
                WORKING_MODEL = m.name  # Ghi nhớ tên model này cho tất cả lần sau!
                return response.text
            except Exception:
                continue
                
        return "Lỗi: Không tìm thấy model AI nào hoạt động với API Key này."
    except Exception as e:
        return f"Lỗi khi gọi AI API: {str(e)}"
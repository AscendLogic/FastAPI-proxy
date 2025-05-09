from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware
import openai
import os
import traceback

app = FastAPI()

# ✅ Enable CORS so the frontend can POST to the backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Replace "*" with your domain in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Serve your HTML frontend at the root route
@app.get("/", response_class=HTMLResponse)
def serve_frontend():
    return FileResponse("index.html")

# ✅ Proxy OpenAI request through your backend
@app.post("/proxy/openai")
async def proxy_openai(request: Request):
    try:
        data = await request.json()

        openai.api_key = os.getenv("JeffersonFisherKey")
        if not openai.api_key:
            raise ValueError("Missing OpenAI API key. Set 'JeffersonFisherKey' in Render environment.")

        # Call OpenAI Chat Completion
        response = openai.chat.completions.create(
        model=data["model"],
        messages=data["messages"],
        max_tokens=data.get("max_tokens", 100)
    )
   

    except Exception as e:
        print("🔥 ERROR in /proxy/openai")
        print("Exception:", e)
        traceback.print_exc()
        return JSONResponse(status_code=500, content={"error": str(e)})
    
    return JSONResponse(content=response.model_dump())
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware
import openai
import os

app = FastAPI()

# Allow CORS (so your frontend can talk to your backend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # You can restrict this later
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve index.html at root
@app.get("/", response_class=HTMLResponse)
def serve_index():
    return FileResponse("index.html")

# Proxy route to OpenAI
@app.post("/proxy/openai")
async def proxy_openai(request: Request):
    try:
        data = await request.json()
        user_id = request.headers.get("X-User-ID", "anonymous")

        openai.api_key = os.getenv("JeffersonFisherKey")
        if not openai.api_key:
            return JSONResponse(status_code=500, content={"error": "Missing OpenAI API key"})

        response = openai.ChatCompletion.create(**data)
        return JSONResponse(content=response)
    
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

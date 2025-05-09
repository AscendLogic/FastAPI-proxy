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
        response = open

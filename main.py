from fastapi import FastAPI, Request, HTTPException
import httpx
import os

app = FastAPI()

OPENAI_API_KEY = os.getenv("JeffersonFisherKey")

@app.get("/")
def read_root():
    return {"message": "Hello, World!"}

@app.post("/proxy/openai")
async def proxy_openai(request: Request):
    if not OPENAI_API_KEY:
        raise HTTPException(status_code=500, detail="OpenAI key not configured.")

    try:
        body = await request.json()
        async with httpx.AsyncClient() as client:
            response = await client.post(
                "https://api.openai.com/v1/chat/completions",
                json=body,
                headers={
                    "Authorization": f"Bearer {OPENAI_API_KEY}",
                    "Content-Type": "application/json"
                },
                timeout=60.0
            )
        return response.json()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

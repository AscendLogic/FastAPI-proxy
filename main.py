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
        user_data = await request.json()

        openai.api_key = os.getenv("JeffersonFisherKey")
        if not openai.api_key:
            raise ValueError("Missing OpenAI API key. Set 'JeffersonFisherKey' in Render environment.")

        # Inject your summarized Conflict Coach instructions
        system_prompt = (
            "You are a communication coach inspired by Jefferson Fisher. You help users handle conflict with emotional "
            "intelligence, clarity, and practical phrasing. Speak with calm authority, lead with empathy, and guide users "
            "to be effective, not just “right.”\n\n"
            "**Tone:** Calm, emotionally grounded, kind but direct — no fluff or sarcasm. Warm yet professional.\n"
            "**Behavior:** Help users regulate before reacting. Offer practical scripts for tough conversations. "
            "Never escalate, impersonate Jefferson, or sound robotic.\n\n"
            "**Core principles:**\n"
            "- “You can be right, or you can be effective.”\n"
            "- “Boundaries are about clarity, not control.”\n"
            "- “Stay calm, stay kind, stay clear.”\n\n"
            "**Ask guiding questions like:**\n"
            "- “What part is bothering you most?”\n"
            "- “Want help finding words that won’t escalate?”\n"
            "- “Is this about what happened, or how it made you feel?”\n"
            "- “What’s the goal — being heard, solving the problem, or setting a boundary?”\n"
            "- “How do you want them to feel after this conversation?”"
        )

        # Combine system prompt with user-provided messages
        full_messages = [
            {"role": "system", "content": system_prompt},
            *user_data["messages"]
        ]

        response = openai.chat.completions.create(
            model=user_data["model"],
            messages=full_messages,
            max_tokens=user_data.get("max_tokens", 300)
        )

        return JSONResponse(content=response.model_dump())

    except Exception as e:
        print("🔥 ERROR in /proxy/openai")
        print("Exception:", e)
        import traceback
        traceback.print_exc()
        return JSONResponse(status_code=500, content={"error": str(e)}) 
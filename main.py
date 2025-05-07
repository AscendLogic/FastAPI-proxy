from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
import os

app = FastAPI()

# Serve index.html
@app.get("/", response_class=HTMLResponse)
def serve_html():
    return FileResponse(os.path.join(os.path.dirname(__file__), "index.html"))
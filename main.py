from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
import os

app = FastAPI()

# Serve index.html
@app.get("/", response_class=HTMLResponse)
def serve_frontend():
    return FileResponse("index.html")

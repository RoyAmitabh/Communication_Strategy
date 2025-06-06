from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse

app = FastAPI()
app.mount("/static", StaticFiles(directory="src/core/static"), name="static")

shared_text = ""

@app.get("/")
async def get():
    return HTMLResponse(open("src/core/static/polling_custom.html").read())

@app.get("/text")
def get_text():
    return {"text": shared_text}

@app.post("/text")
async def update_text(request: Request):
    global shared_text
    data = await request.json()
    shared_text = data.get("text", "")
    return {"status": "updated"}

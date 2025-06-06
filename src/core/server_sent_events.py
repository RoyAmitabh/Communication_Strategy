from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
import asyncio
import time

app = FastAPI()
app.mount("/static", StaticFiles(directory="src/core/static"), name="static")

@app.get("/")
async def root():
    return HTMLResponse(open("src/core/static/sse_demo.html").read())

@app.get("/events")
async def stream_events(request: Request):
    async def event_generator():
        i = 0
        while True:
            # If client disconnects, stop the loop
            if await request.is_disconnected():
                break
            # Yield a message every second
            yield f"data: Server Time: {time.strftime('%H:%M:%S')}, Count: {i}\n\n"
            await asyncio.sleep(1)
            i += 1

    return StreamingResponse(event_generator(), media_type="text/event-stream")

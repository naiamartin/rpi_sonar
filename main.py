from fastapi import FastAPI, HTTPException, Body, Request
from pydantic import BaseModel
from typing import List, Optional
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import os
from pathlib import Path

PACIFICO, FACIL, NORMAL, DIFICIL, ALMONDIGA = 0, 1, 2, 3, 4
dificultad = NORMAL

app = FastAPI()
current_sensor_data = 0.0
current_led_data = {
    "led_r":True,
    "led_v":False
}

# CORS permite peticiones desde HTML
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)
path = os.getcwd()+"/static"
app.mount("/static", StaticFiles(directory=path), name="static")

templates = Jinja2Templates(directory="static/templates")

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/sensor/current")
async def get_current_sensor():
    #estado actual
    if current_sensor_data is None:
        raise HTTPException(status_code=404, detail="No hay datos del sensor disponibles")
    return current_sensor_data


@app.post("/sensor/update")
async def update_sensor(distance:float = Body(...)):
    #actualiza datos del sensor
    global current_sensor_data
    
    current_sensor_data = distance
    return distance

@app.get("/led/current")
async def get_current_leds():
    #estado actual
    if current_sensor_data is None:
        raise HTTPException(status_code=404, detail="No hay datos del led disponibles")
    return current_led_data

@app.post("/led/update")
async def update_led(data:dict):
    #actualiza datos del sensor
    global current_led_data
    
    current_led_data["led_r"] = data["led_r"]
    current_led_data["led_v"] = data["led_v"]
    return current_led_data

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

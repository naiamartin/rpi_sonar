from fastapi import FastAPI, HTTPException, Body, Request
from pydantic import BaseModel
from typing import List, Optional
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import os
from pathlib import Path


app = FastAPI()

current_sensor_data = {"distance":0.0}
juego = {"jugando":True}
estado = {"estado":0}

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

@app.get("/derrota", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("derrota.html", {"request": request})

@app.get("/victoria", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("victoria.html", {"request": request})


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
    
    current_sensor_data["distance"] = distance
    return distance

@app.post("/game/playing")
async def setgame(jugando:dict):
    global juego
    juego = jugando

@app.get("/game/jugando")
async def leerjuego():
    return juego

@app.post("status/actual")
async def actualizar(status:dict):
    global estado
    estado = status

@app.get("/status/leer")
async def leerstatus():
    return estado

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

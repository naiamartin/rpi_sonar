from fastapi import FastAPI, HTTPException, Body, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pathlib import Path

app = FastAPI()

current_sensor_data = {"distance": 120.0}
juego = {"jugando": True}
estado_juego = {"estado": 0}  # 0=jugando, 1=victoria, 2=derrota

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

static_dir = Path(__file__).parent / "static"
templates_dir = Path(__file__).parent / "static" / "templates"

app.mount("/static", StaticFiles(directory=static_dir), name="static")
templates = Jinja2Templates(directory=str(templates_dir))

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    if estado_juego["estado"] == 1:
        return RedirectResponse("/victoria")
    elif estado_juego["estado"] == 2:
        return RedirectResponse("/derrota")
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/victoria", response_class=HTMLResponse)
async def victoria(request: Request):
    if estado_juego["estado"] != 1:
        estado_juego["estado"] = 1
    return templates.TemplateResponse("victoria.html", {"request": request})

@app.get("/derrota", response_class=HTMLResponse)
async def derrota(request: Request):
    if estado_juego["estado"] != 2:
        estado_juego["estado"] = 2
    return templates.TemplateResponse("derrota.html", {"request": request})

@app.get("/status/leer")
async def leer_estado():
    return estado_juego

@app.post("/status/update")
async def actualizar_estado(estado_nuevo: int = Body(...)):
    global estado_juego, juego
    estado_juego["estado"] = estado_nuevo
    
    if estado_nuevo != 0:
        juego["jugando"] = False
    else:
        juego["jugando"] = True
    
    return {"estado": estado_nuevo}

@app.post("/game/reset")
async def reset_game():
    global estado_juego, juego, current_sensor_data
    estado_juego["estado"] = 0
    juego["jugando"] = True
    current_sensor_data["distance"] = 120.0
    return {"mensaje": "Juego reiniciado"}

@app.get("/sensor/current")
async def get_current_sensor():
    if current_sensor_data is None:
        raise HTTPException(status_code=404, detail="No hay datos del sensor disponibles")
    return current_sensor_data

@app.post("/sensor/update")
async def update_sensor(distance: float = Body(...)):
    global current_sensor_data
    current_sensor_data["distance"] = distance
    return distance

@app.post("/game/playing")
async def setgame(jugando: dict):
    global juego
    juego = jugando

@app.get("/game/jugando")
async def leerjuego():
    return juego

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
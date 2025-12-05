from fastapi import FastAPI, HTTPException
from gpiozero.pins.lgpio import LGPIOFactory
from pydantic import BaseModel
from typing import List, Optional
from fastapi.middleware.cors import CORSMiddleware
from gpiozero import DistanceSensor, LED, Buzzer
import threading, queue, time
import random

led_r = LED(26)
led_v = LED(5)
sensor = DistanceSensor(echo=23, trigger=22)
buzz = Buzzer(17)
eventos = queue.Queue()
CORRER, PARAR, FIN = 0, 1, 2
estado = CORRER # estado inicia
PACIFICO, FACIL, NORMAL, DIFICIL, ALMONDIGA = 0, 1, 2, 3, 4
dificultad = FACIL
ran = 0

API_URL = "http://localhost:8000" 

#“Daemon thread” que envía un evento anta cada pulsación
def manejador():
    global dificultad
    global ran
    if dificultad == PACIFICO:
        eventos.put("CORRER")
    elif dificultad == FACIL:
        while estado != FIN:
            eventos.put("CORRER")
            ran = random.randint(2,5)
            time.sleep(ran)
            eventos.put("PARAR")
            ran = random.randint(1,3)
            time.sleep(ran)
    elif dificultad == NORMAL:
        while estado != FIN:
            eventos.put("CORRER")
            ran = random.randint(1,4)
            time.sleep(ran)
            eventos.put("PARAR")
            ran = random.randint(1,4)
            time.sleep(ran)
    elif dificultad == DIFICIL:
        while estado != FIN:
            eventos.put("CORRER")
            ran = random.randint(1,3)
            time.sleep(ran)
            eventos.put("PARAR")
            ran = random.randint(2,5)
            time.sleep(ran)
    elif dificultad == ALMONDIGA:
        while estado != FIN:
            eventos.put("CORRER")
            ran = random.randint(1,2)
            time.sleep(ran)
            eventos.put("PARAR")
            ran = random.randint(3,6)
            time.sleep(ran)

def led_worker():
    global estado
    global t_leer
    while True:
        if estado == CORRER:
            led_v.on()
            led_r.off()
        elif estado == PARAR:
            led_v.off()
            led_r.on()
            distanciavieja = sensor.distance *100
            for i in range (ran*20):
                if abs(sensor.distance*100 - distanciavieja) >= 5:
                    eventos.put("FIN")
                    print("ALAAAA")
                    break
                time.sleep(0.05)
        elif estado == FIN:
            buzz.on()
            time.sleep(0.2)
            buzz.off()
            for _ in range(5):
                led_r.toggle()
                led_v.toggle()
                time.sleep(0.2)
            break
        
        

t_manejador = threading.Thread(target=manejador,daemon=True)
t_led = threading.Thread(target=led_worker, daemon=True)
t_manejador.start()
t_led.start()
while estado != FIN:
    evento = eventos.get()
    if evento == "CORRER" :
        estado = CORRER
    elif evento == "PARAR":
        estado = PARAR
    elif evento == "FIN":
        estado = FIN
    print(estado)

print("FIn")


class SensorData(BaseModel):
    distance: float
    led_status: str  # "GREEN", "RED"
    game_status: str  # "jugando", "game_over", "interrumpido"
    timestamp: float

app = FastAPI()

# CORS permite peticiones desde HTML
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

current_sensor_data: Optional[SensorData] = None
MAX_HISTORY = 100

@app.get("/")
async def root():
    return {
        "message": "Red Light Green Light API funcionando",
        "current_status": current_sensor_data.game_status if current_sensor_data else "no_data"
    }

@app.get("/sensor/current")
async def get_current_sensor():
    #estado actual
    if current_sensor_data is None:
        raise HTTPException(status_code=404, detail="No hay datos del sensor disponibles")
    return current_sensor_data


@app.post("/sensor/update")
async def update_sensor(data: SensorData):
    #actualiza datos del sensor
    global current_sensor_data
    
    current_sensor_data = data
    sensor_history.append(data)
    
    if len(sensor_history) > MAX_HISTORY:
        sensor_history.pop(0)
    
    return {"status": "ok", "data": data}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

@app.post("/game/reset")
async def game_reset():
    global current_sensor_data
    current_sensor_data = None
    return {"status": "reset"}

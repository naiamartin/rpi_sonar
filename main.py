from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from fastapi.middleware.cors import CORSMiddleware

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
sensor_history: List[SensorData] = []
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
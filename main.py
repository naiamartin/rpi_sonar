from fastapi import FastAPI
from pydantic import BaseModel
from typing import List


class Point(BaseModel):
    angle: int
    distance: int 
    

app = FastAPI()
# Simular puntos(almacen global)
current_points: List[Point] = [
    Point(angle=70, distance = 120),
    Point(angle=120, distance=80)
]

@app.get("/points")
async def get_point():
    return current_points

@app.post("/points/")
async def create_point(point: Point):
    current_points.append(point)
    return point
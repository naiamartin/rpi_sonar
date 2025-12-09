from gpiozero import DistanceSensor, LED, Buzzer
import threading, queue, time, requests, json
import random
led_r = LED(26)
led_v = LED(5)
sensor = DistanceSensor(echo=23, trigger=22)
buzz = Buzzer(17)
eventos = queue.Queue()
CORRER, PARAR, FIN = 0, 1, 2
estado = CORRER # estado inicia
PACIFICO, FACIL, NORMAL, DIFICIL, ALMONDIGA = 0, 1, 2, 3, 4
dificultad = NORMAL
ran = 0

API_URL = "http://localhost:8000" 

#“Daemon thread” que envía un evento anta cada pulsación
def manejador():
    global dificultad
    global ran

    data = requests.get(f"{API_URL}/game/jugando").content.decode('utf-8')

    data = json.loads(data)

    jugando = data["jugando"]
    print(jugando)

    if led_r:
        eventos.put("PARAR")
    elif led_v:
        eventos.put("CORRER")
    elif led_r and led_v:
        eventos.put("FIN")

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
            while evento == PARAR:
                if abs(sensor.distance*100 - distanciavieja) >= 5:
                    requests.post(f"{API_URL}/led/update", json={"led_r":True, "led_v":True})
                    print("ALAAAA")
                    break
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
from gpiozero import DistanceSensor, LED, Buzzer
import threading, queue, time, requests, json

led_r = LED(26)
led_v = LED(5)
sensor = DistanceSensor(echo=23, trigger=22)
buzz = Buzzer(17)
eventos = queue.Queue()
CORRER, PARAR = 0, 1
VICTORIA, DERROTA = 1, 2
estado = CORRER
estado_juego = 0

API_URL = "http://localhost:8000"

def manejador():
    global estado_juego
    while True:
        try:
            requests.post(f"{API_URL}/sensor/update", json=sensor.distance * 100)

            if sensor.distance * 100 <= 5 and estado_juego == 0:
                estado_juego = 1
                requests.post(f"{API_URL}/status/update", json=estado_juego)
                eventos.put("VICTORIA")
                continue

            data = requests.get(f"{API_URL}/game/jugando").content.decode('utf-8')
            data = json.loads(data)
            jugando = data["jugando"]

            if jugando and estado_juego == 0:
                eventos.put("CORRER")
            elif not jugando and estado_juego == 0:
                eventos.put("PARAR")
                
        except Exception as e:
            time.sleep(0.1)

def led_worker():
    global estado, estado_juego
    while True:
        if estado == CORRER and estado_juego == 0:
            led_v.on()
            led_r.off()
            buzz.off()
            
        elif estado == PARAR and estado_juego == 0:
            led_v.off()
            led_r.on()
            distanciavieja = sensor.distance * 100
            
            while estado == PARAR and estado_juego == 0:
                if abs(sensor.distance * 100 - distanciavieja) >= 2:
                    estado_juego = 2
                    try:
                        requests.post(f"{API_URL}/status/update", json=estado_juego)
                    except:
                        pass
                    eventos.put("DERROTA")
                    break
                    
                time.sleep(0.1)
                
        elif estado_juego == VICTORIA:
            for _ in range(10):
                led_v.on()
                led_r.off()
                time.sleep(0.2)
                led_v.off()
                led_r.on()
                time.sleep(0.2)
            break
            
        elif estado_juego == DERROTA:
            for _ in range(2):
                buzz.on()
                led_r.on()
                led_v.off()
                time.sleep(0.2)
                buzz.off()
                led_r.off()
                time.sleep(0.2)
            break

t_manejador = threading.Thread(target=manejador, daemon=True)
t_led = threading.Thread(target=led_worker, daemon=True)
t_manejador.start()
t_led.start()

while estado_juego == 0:
    evento = eventos.get()
    if evento == "CORRER":
        estado = CORRER
    elif evento == "PARAR":
        estado = PARAR
    elif evento == "VICTORIA":
        estado_juego = VICTORIA
        break
    elif evento == "DERROTA":
        estado_juego = DERROTA
        break
        
time.sleep(3)


from gpiozero import DistanceSensor, LED, Buzzer
from time import sleep, time
import random
import requests
import threading

API_URL = "http://localhost:8000" 

# Configuracion de GPIO
sensor = DistanceSensor(echo=23, trigger=22)
led_r = LED(26)
led_v = LED(5)
buzz = Buzzer(17)

#Variables de estado
acabado = False
current_distance = 0
current_led_status = "OFF"
current_game_status = "waiting"

def send_sensor_data():
    #Envía datos del sensor a la API
    try:
        data = {
            "distance": current_distance,
            "led_status": current_led_status,
            "game_status": current_game_status,
            "timestamp": time()
        }
        requests.post(f"{API_URL}/sensor/update", json=data, timeout=1)
    except Exception as e:
        print(f"Error enviando datos a la API: {e}")

def update_sensor_loop():
    #Loop en segundo plano para actualizar datos del sensor constantemente
    global current_distance
    while not acabado:
        try:
            current_distance = round(sensor.distance * 100, 2)
            send_sensor_data()
        except Exception as e:
            print(f"Error leyendo sensor: {e}")
        sleep(0.1)  #100ms

#Inicializar LEDs
led_r.off()
led_v.off()
buzz.off()

#Iniciar thread para actualización constante del sensor
sensor_thread = threading.Thread(target=update_sensor_loop, daemon=True)
sensor_thread.start()

print("=== Luz verde luz roja ===")
print(f"API conectada en: {API_URL}")
current_game_status = "jugando"

try:
    while not acabado:
        #Luz verde
        led_v.on()
        led_r.off()
        current_led_status = "GREEN"
        print("Muévete, luz verde (okomako...)")
        sleep(random.randint(1, 4))
        
        #Luz roja
        led_v.off()
        led_r.on()
        current_led_status = "RED"
        print("¡Quieto!")
        
        #Guardar distancia inicial
        distanciavieja = sensor.distance * 100
        
        #verificar movimiento durante 4 segundos(20 veces)
        for _ in range(20):
            distancia_actual = sensor.distance * 100
            
            if abs(distancia_actual - distanciavieja) >= 5:
                print("¡MUERTO! Te has movido")
                current_game_status = "game_over"
                send_sensor_data()
                
                buzz.on()
                sleep(0.2)
                buzz.off()
                
                #Parpadeo de luces
                for j in range(20):
                    led_r.toggle()
                    led_v.toggle()
                    sleep(0.1)
                
                acabado = True
                break
            
            sleep(0.2)
        
        led_r.off()
        buzz.off()

except KeyboardInterrupt:
    print("\nJuego interrumpido")
    current_game_status = "interrumpido"
    send_sensor_data()

finally:
    led_r.off()
    led_v.off()
    buzz.off()
    current_led_status = "OFF"
    if not acabado:
        current_game_status = "interrumpido"
    send_sensor_data()
    print("Fin del juego")
    print("Datos enviados a la API. Revisar en http://localhost:8000/docs")
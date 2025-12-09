
const API_URL = "http://localhost:8000"; // Cambia si la API está en otra IP

// Elementos HTML
const luzRoja = document.getElementById("luz-roja");
const luzVerde = document.getElementById("luz-verde");
const punto = document.getElementById("punto");

// Función para actualizar LEDs
async function actualizarLeds() {
try {
    const res = await fetch(`${API_URL}/game/jugando`);
    const data = await res.json();
    if(data.jugando){
        luzVerde.style.backgroundColor = "rgb(0,200,0)";
        luzRoja.style.backgroundColor = "rgb(50,50,50)";
    }else{
        luzVerde.style.backgroundColor = "rgb(50,50,50)";
        luzRoja.style.backgroundColor = "rgb(255, 0, 0)";
    }

} catch (err) {
    console.error("Error al leer LEDs:", err);
}
}

// Función para actualizar distancia
async function actualizarDistancia() {
try {
    const res = await fetch(`${API_URL}/sensor/current`);
    const data = await res.json();

    //const data = {'distance':97};

    // Mover el "punto" según la distancia
    const maxDist = 150; // distancia máxima
    const minDist = 5;
    const dist = Math.min(Math.max(data.distance, minDist), maxDist);
    const porcentaje = 1 - (dist / maxDist);
    const maxPx = 1100; // ancho máximo en px
    const posX = porcentaje * maxPx;
    
    punto.style.transform = `translateX(${posX}px)`;
} catch (err) {
    console.error("Error al leer distancia:", err);
}
}

// Actualizar todo cada 100ms 
setInterval(() => {
actualizarLeds();
actualizarDistancia();
}, 100);

async function cambiarModo() {
    try {
    const res = await fetch(`${API_URL}/game/jugando`);
    const data = await res.json();
    
    if(data.jugando){
        await fetch(`${API_URL}/game/playing`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({jugando: false})
        });
    }else{
        await fetch(`${API_URL}/game/playing`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({jugando: true})
        });
    }
    } catch (err) {
        console.error("Error al leer estado de juego:", err);
    }

}

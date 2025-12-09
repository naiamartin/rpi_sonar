
const API_URL = "http://localhost:8000"; // Cambia si la API está en otra IP

// Elementos HTML
const luzRoja = document.getElementById("luz-roja");
const luzVerde = document.getElementById("luz-verde");
const punto = document.getElementById("punto");

// Función para actualizar LEDs
async function actualizarLeds() {
try {
    //const res = await fetch(`${API_URL}/led/current`);
    //const data = await res.json();

    const data = {"led_v": true, "led_r": false}

    // Cambiar color según estado
    luzVerde.style.backgroundColor = data.led_v ? "rgb(0,200,0)" : "rgb(50,50,50)";
    luzRoja.style.backgroundColor  = data.led_r ? "rgb(255,0,0)" : "rgb(50,50,50)";
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
    const maxPx = 500; // ancho máximo en px
    const posX = porcentaje * maxPx;
    
    punto.style.transform = `translateX(${data.distance}px)`;
} catch (err) {
    console.error("Error al leer distancia:", err);
}
}

// Actualizar todo cada 100ms 
setInterval(() => {
actualizarLeds();
actualizarDistancia();
}, 100);

async function encenderVerde() {
    await fetch(`${API_URL}/led/update`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ led_v: true, led_r: false })
    });

    luzVerde.style.backgroundColor = "rgb(0,255,0)";
    luzRoja.style.backgroundColor = "rgb(50,50,50)";
}
async function apagarVerde() {
    await fetch(`${API_URL}/led/update`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ led_v: false, led_r: false })
    });
    luzVerde.style.backgroundColor = "rgb(50,50,50)";
}

async function encenderRoja() {
    await fetch(`${API_URL}/led/update`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ led_v: false, led_r: true })
    });

    luzRoja.style.backgroundColor = "rgb(255,0,0)";
    luzVerde.style.backgroundColor = "rgb(50,50,50)";
}

async function apagarRoja() {
    await fetch(`${API_URL}/led/update`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ led_v: false, led_r: false })
    });

    luzRoja.style.backgroundColor = "rgb(50,50,50)";
}
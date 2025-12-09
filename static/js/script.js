const API_URL = "http://localhost:8000";

// Elementos HTML
const luzRoja = document.getElementById("luz-roja");
const luzVerde = document.getElementById("luz-verde");
const punto = document.getElementById("punto");
const botonCambiar = document.getElementById("boton-cambiar-led");

let estadoAnterior = -1;
let jugando = true;

// Función para actualizar LEDs
async function actualizarLeds() {
    try {
        const res = await fetch(`${API_URL}/game/jugando`);
        const data = await res.json();
        jugando = data.jugando;
        
        if (jugando) {
            luzVerde.style.backgroundColor = "rgb(0,200,0)";
            luzRoja.style.backgroundColor = "rgb(50,50,50)";
            botonCambiar.textContent = "PARAR";
        } else {
            luzVerde.style.backgroundColor = "rgb(50,50,50)";
            luzRoja.style.backgroundColor = "rgb(255, 0, 0)";
            botonCambiar.textContent = "CONTINUAR";
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

        const maxDist = 150;
        const minDist = 5;
        const dist = Math.min(Math.max(data.distance, minDist), maxDist);
        const porcentaje = 1 - (dist / maxDist);
        const maxPx = 1400;
        const posX = porcentaje * maxPx;
        
        punto.style.transform = `translateX(${posX}px)`;
    } catch (err) {
        console.error("Error al leer distancia:", err);
    }
}

// Función para cambiar modo
async function cambiarModo() {
    try {
        const res = await fetch(`${API_URL}/game/jugando`);
        const data = await res.json();

        const nuevoEstado = !data.jugando;
        await fetch(`${API_URL}/game/playing`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({jugando: nuevoEstado})
        });
    } catch (err) {
        console.error("Error al cambiar modo:", err);
    }
}

// Función para verificar estado
async function actualizarEstado() {
    try {
        const res = await fetch(`${API_URL}/status/leer`);
        const data = await res.json();
        
        if (data.estado !== estadoAnterior) {
            estadoAnterior = data.estado;
            
            if (data.estado === 0) {
                if (!window.location.pathname.endsWith("/")) {
                    window.location.href = "/";
                }
            } else if (data.estado === 1) {
                if (!window.location.pathname.endsWith("/victoria")) {
                    window.location.href = "/victoria";
                }
            } else if (data.estado === 2) {
                if (!window.location.pathname.endsWith("/derrota")) {
                    window.location.href = "/derrota";
                }
            }
        }
    } catch (err) {
        console.error("Error al leer estado:", err);
    }
}

// Función para reiniciar juego
async function comenzarJuego() {
    try {
        await fetch(`${API_URL}/game/reset`, {
            method: "POST"
        });
        window.location.href = "/";
    } catch (err) {
        console.error("Error al reiniciar juego:", err);
    }
}

// Detectar en qué página estamos
const currentPath = window.location.pathname;

if (currentPath.includes("victoria") || currentPath.includes("derrota")) {
    // Página de resultado
    setInterval(actualizarEstado, 500);
    
    // Verificar si debemos volver al juego
    setInterval(async () => {
        try {
            const res = await fetch(`${API_URL}/status/leer`);
            const data = await res.json();
            if (data.estado === 0 && !currentPath.endsWith("/")) {
                window.location.href = "/";
            }
        } catch (err) {
            console.error("Error verificando estado:", err);
        }
    }, 1000);
    
} else {
    // Página principal
    setInterval(actualizarEstado, 500);
    setInterval(() => {
        actualizarLeds();
        actualizarDistancia();
    }, 100);
}
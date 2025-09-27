# Ratoncito Pérez — Fullstack local run

Este repositorio contiene un backend en FastAPI (carpeta `backend/`) y un frontend en React (carpeta `frontend/`).

Instrucciones rápidas para desarrollo en macOS / Linux:

1) Backend

- Crear y activar un entorno virtual (recomiendo venv/virtualenv)

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r backend/requirements.txt
```

- (Opcional) añade tus claves en `backend/.env`, por ejemplo `GROQ_API_KEY` o `OPENWEATHER_API_KEY`.

- Iniciar el backend:

```bash
# desde la raiz del proyecto
python -m uvicorn backend.main:app --host 0.0.0.0 --port 8000 --reload
```

2) Frontend

- Instalar dependencias y ejecutar (Create React App):

```bash
cd frontend
npm install
npm start
```

- En desarrollo el frontend usa un proxy (configurado en `frontend/package.json`) que reenvía peticiones a `http://localhost:8000`. Alternativamente puedes fijar la url del API con la variable de entorno `REACT_APP_API_URL` (por ejemplo para apuntar a un backend remoto):

```bash
# Usar backend local en desarrollo (proxy) - no hace falta REACT_APP_API_URL
npm start

# O probar contra un backend en otra URL
REACT_APP_API_URL=https://mi-backend.example.com npm start
```

3) Script de conveniencia

- Hay un script `start_servers.py` que intenta arrancar el backend y el frontend de forma portable usando el Python actual y `npm start` (si está disponible). Ejecuta desde la raiz:

```bash
python start_servers.py
```

Notas de conexión y endpoints principales

- Endpoint principal de chat: POST /chat
- Endpoint para explicación educativa del juego: POST /game/crew-explain
- Endpoint health: GET /health
- Frontend development proxy: `http://localhost:3000` -> `http://localhost:8000`

Si quieres, puedo:
- Probar localmente la conexión (si me pides que ejecute comandos aquí)
- Añadir un ejemplo de petición desde el frontend
- Restringir CORS en `backend/src/api/main.py` a la URL de producción

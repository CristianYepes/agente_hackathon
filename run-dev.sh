#!/bin/bash

echo "🚀 Iniciando Ratoncito Pérez - Guía Mágico de Madrid"

# Verificar si existe el entorno virtual del backend
if [ ! -d "backend/venv" ]; then
    echo "❌ No se encontró el entorno virtual. Ejecuta: cd backend && python -m venv venv && source venv/bin/activate && pip install -r requirements.txt"
    exit 1
fi

# Función para cleanup
cleanup() {
    echo "🛑 Deteniendo servicios..."
    kill $BACKEND_PID $FRONTEND_PID 2>/dev/null
    exit 0
}

trap cleanup SIGINT

# Iniciar backend
echo "🐍 Iniciando backend..."
cd backend
source venv/bin/activate
python -m uvicorn src.api.main:app --reload --host 0.0.0.0 --port 8000 &
BACKEND_PID=$!
cd ..

# Esperar un momento para que el backend arranque
sleep 5

# Iniciar frontend
echo "⚛️ Iniciando frontend..."
cd frontend
npm i
npm start &
FRONTEND_PID=$!
cd ..

echo "✅ Servicios iniciados:"
echo "   Backend: http://localhost:8000"
echo "   Frontend: http://localhost:3000"
echo "   API Docs: http://localhost:8000/docs"
echo ""
echo "Presiona Ctrl+C para detener ambos servicios"

# Mantener el script corriendo
wait $BACKEND_PID
wait $FRONTEND_PID

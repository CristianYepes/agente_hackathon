# 🧪 Guía de Pruebas - Ratoncito Pérez

## 🗺️ Detección de Ubicación

### Frontend → Backend Flow:
1. **Frontend (JavaScript)**: `navigator.geolocation.getCurrentPosition()`
2. **Obtiene**: `{latitude: 40.4155, longitude: -3.7074}`
3. **Envía al Backend**: `POST /location/detect`
4. **Backend procesa**: Geocoding + enriquecimiento
5. **Retorna**: Nombre del lugar + contexto

### 🔌 Endpoint: `/location/detect`

**Método**: POST
**URL**: `http://localhost:8000/location/detect`
**Body**:
```json
{
  "latitude": 40.4155,
  "longitude": -3.7074
}
```

**Respuesta**:
```json
{
  "detected_location": {
    "place_name": "Plaza Mayor",
    "raw_place": "Casa de la Panadería",
    "location_type": "plaza",
    "coordinates": {"lat": 40.4155, "lon": -3.7074}
  },
  "is_madrid": true
}
```

## 🎯 Coordenadas de Prueba (Madrid)

### Plaza Mayor
```bash
Invoke-RestMethod -Uri "http://localhost:8000/location/detect" -Method POST -ContentType "application/json" -Body '{"latitude": 40.4155, "longitude": -3.7074}'
```

### Palacio Real
```bash
Invoke-RestMethod -Uri "http://localhost:8000/location/detect" -Method POST -ContentType "application/json" -Body '{"latitude": 40.4179, "longitude": -3.7142}'
```

### Parque del Retiro
```bash
Invoke-RestMethod -Uri "http://localhost:8000/location/detect" -Method POST -ContentType "application/json" -Body '{"latitude": 40.4153, "longitude": -3.6844}'
```

### Puerta del Sol
```bash
Invoke-RestMethod -Uri "http://localhost:8000/location/detect" -Method POST -ContentType "application/json" -Body '{"latitude": 40.4168, "longitude": -3.7038}'
```

## 💬 Chat Completo con Ratoncito Pérez

### Endpoint: `/chat`

**Método**: POST
**URL**: `http://localhost:8000/chat`
**Body completo**:
```json
{
  "message": "¿Qué hay interesante aquí?",
  "location": {
    "latitude": 40.4155,
    "longitude": -3.7074,
    "place_name": "Plaza Mayor"
  },
  "family_profile": {
    "children": [
      {
        "age": 6,
        "gender": "girl",
        "name": "María"
      },
      {
        "age": 8,
        "gender": "boy",
        "name": "Carlos"
      }
    ],
    "language": "es",
    "interests": ["historia", "leyendas"]
  }
}
```

### 🎮 Prueba con PowerShell:
```powershell
$body = @{
  message = "¿Qué secretos tiene este lugar?"
  location = @{
    latitude = 40.4155
    longitude = -3.7074
    place_name = "Plaza Mayor"
  }
  family_profile = @{
    children = @(
      @{
        age = 6
        gender = "girl" 
        name = "Ana"
      }
    )
    language = "es"
    interests = @("historia", "leyendas")
  }
} | ConvertTo-Json -Depth 3

Invoke-RestMethod -Uri "http://localhost:8000/chat" -Method POST -ContentType "application/json" -Body $body
```

## 🌐 Frontend - Detección Automática

### Cómo funciona en el navegador:

1. **Abrir**: http://localhost:8000
2. **Permitir ubicación GPS** cuando el navegador lo pida
3. **Configurar familia**: Edades y géneros
4. **¡Automático!**: El frontend detecta ubicación cada 60 segundos

### JavaScript del Frontend:
```javascript
// En app.js - línea ~89
navigator.geolocation.getCurrentPosition(
  (position) => {
    const { latitude, longitude } = position.coords;
    // Envía automáticamente al backend
    fetch('/location/detect', {
      method: 'POST',
      body: JSON.stringify({ latitude, longitude })
    });
  },
  (error) => console.error('GPS error:', error),
  { enableHighAccuracy: true, timeout: 10000 }
);
```

## 🔍 Otros Endpoints Útiles

### Health Check
```bash
Invoke-RestMethod -Uri "http://localhost:8000/health" -Method GET
```

### Ubicaciones Populares
```bash
Invoke-RestMethod -Uri "http://localhost:8000/madrid-locations" -Method GET
```

### API Docs (Swagger)
**URL**: http://localhost:8000/docs

## 🎯 Flujo Completo de Prueba

1. **Verificar servidor**: `GET /health`
2. **Probar ubicación**: `POST /location/detect` con coordenadas
3. **Chat completo**: `POST /chat` con perfil familiar
4. **Frontend**: Abrir navegador y permitir GPS
5. **Interactuar**: Chatear con el Ratoncito Pérez

¡Ahora ya sabes exactamente cómo funciona y probar cada parte! 🐭✨

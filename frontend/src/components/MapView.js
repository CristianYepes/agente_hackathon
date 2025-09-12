import React, { useState, useRef, useEffect } from 'react';
import { MapContainer, TileLayer, Marker, Popup, ZoomControl, LayersControl, useMap } from 'react-leaflet';
import L from 'leaflet';

import ModalPermission from './ModalPermission';
import FilterModal from './FilterModal';
import { iniciarGeolocalizacion, LocationPermissionState, checkPermissionState, pedirPermisos } from '../handlers/location';

// Fix para los iconos de Leaflet
delete L.Icon.Default.prototype._getIconUrl;
L.Icon.Default.mergeOptions({
  iconRetinaUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-icon-2x.png',
  iconUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-icon.png',
  shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-shadow.png',
});

// Función para crear iconos personalizados
const createCustomIcon = (emoji, color) => {
  return L.divIcon({
    html: `<div style="background-color: ${color}; width: 32px; height: 32px; border-radius: 50%; border: 3px solid white; box-shadow: 0 3px 10px rgba(0,0,0,0.4); display: flex; align-items: center; justify-content: center; font-size: 16px; cursor: pointer;">${emoji}</div>`,
    className: 'custom-marker-icon',
    iconSize: [32, 32],
    iconAnchor: [16, 16],
    popupAnchor: [0, -16]
  });
};

// Componente para centrar el mapa en la ubicación del usuario
const LocationMarker = ({ position }) => {
  const map = useMap();

  return position ? (
    <Marker
      position={position}
      icon={createCustomIcon('📍', '#2563eb')}
      eventHandlers={{
        click: (e) => {
          map.flyTo(e.latlng, 14);
        },
      }}
    >
      <Popup>
        <div className="text-center">
          <h4 className="font-bold">Tu ubicación</h4>
          <p className="text-sm text-gray-600">
            Lat: {position[0].toFixed(6)}<br />
            Lon: {position[1].toFixed(6)}
          </p>
        </div>
      </Popup>
    </Marker>
  ) : null;
};

const MapController = ({ onMapReady }) => {
  const map = useMap();
  useEffect(() => {
    if (map) onMapReady(map);
  }, [map, onMapReady]);
  return null;
};

const MapView = () => {
  const [selectedPoint, setSelectedPoint] = useState(null);
  const [activeFilter, setActiveFilter] = useState('all');
  const [showFilterModal, setShowFilterModal] = useState(false);
  const [userLocation, setUserLocation] = useState(null);
  const [showLocationPrompt, setShowLocationPrompt] = useState(false);
  const [map, setMap] = useState(null);
  const [permissionsGranted, setPermissionsGranted] = useState(false);

  // Efecto para iniciar el seguimiento de ubicación
  useEffect(() => {
    let stopTracking = null;
    let retryTimeout = null;
    let retryCount = 0;
    const MAX_RETRIES = 3;

    const checkPermissions = async () => {
      const state = await checkPermissionState();
      if (state === 'granted') {
        setPermissionsGranted(true);
        setShowLocationPrompt(false); // no mostrar modal
      } else {
        setPermissionsGranted(false);
        setShowLocationPrompt(true); // mostrar modal
      }
    };

    checkPermissions();

    const startLocationTracking = () => {
      if (retryCount >= MAX_RETRIES) {
        console.warn("Se alcanzó el máximo número de reintentos para el tracking de ubicación");
        return;
      }

      stopTracking = iniciarGeolocalizacion(
        (newLocation) => {
          checkPermissions();
          console.log("Nueva ubicación:", newLocation);
          setUserLocation([newLocation.latitude, newLocation.longitude]);
          retryCount = 0; // Resetear contador de reintentos si tuvimos éxito
        },
        (error) => {
          console.warn("Error al actualizar ubicación:", error);
          retryCount++;

          // Intentar reiniciar el tracking después de un tiempo
          if (retryCount < MAX_RETRIES) {
            console.log(`Reintentando tracking (intento ${retryCount + 1}/${MAX_RETRIES})...`);
            retryTimeout = setTimeout(() => {
              if (stopTracking) stopTracking();
              startLocationTracking();
            }, 10000); // Esperar 10 segundos antes de reintentar
          }
        }
      );
    };

    if (permissionsGranted) {
      startLocationTracking();
    }

    // Limpieza al desmontar
    return () => {
      if (stopTracking) stopTracking();
      if (retryTimeout) clearTimeout(retryTimeout);
    };
  }, [permissionsGranted]);

  // Coordenadas de Madrid
  const madridPosition = [40.4168, -3.7038];

  // Categorías
  const categories = [
    { id: 'all', name: 'Todos', color: '#6b7280' },
    { id: 'historic', name: 'Históricos', color: '#dc2626' },
    { id: 'museum', name: 'Museos', color: '#7c3aed' },
    { id: 'park', name: 'Parques', color: '#059669' },
    { id: 'palace', name: 'Palacios', color: '#f59e0b' }
  ];

  // Puntos de interés con emojis
  const pointsOfInterest = [
    {
      id: 1,
      position: [40.4168, -3.7038],
      title: "Casa del Ratoncito Pérez",
      description: "¡Aquí el Ratoncito Pérez recoge muchos dientes! ¿Sabías que vivía en la calle del Arenal?",
      type: "historic",
      icon: createCustomIcon('🦷', '#dc2626')
    },
    {
      id: 2,
      position: [40.4173, -3.7061],
      title: "Plaza Mayor",
      description: "¡El lugar donde el Ratoncito Pérez conoce a todos los gatos de Madrid!",
      type: "historic",
      icon: createCustomIcon('🧀', '#dc2626')
    },
    {
      id: 3,
      position: [40.4202, -3.7058],
      title: "Palacio Real",
      description: "¡El castillo donde el Ratoncito Pérez conoció al Rey Alfonso XIII!",
      type: "palace",
      icon: createCustomIcon('👑', '#f59e0b')
    },
    {
      id: 4,
      position: [40.4138, -3.6921],
      title: "Parque del Retiro",
      description: "El parque favorito del Ratoncito para jugar y esconder tesoros",
      type: "park",
      icon: createCustomIcon('🧀', '#059669')
    },
    {
      id: 5,
      position: [40.4096, -3.6918],
      title: "Museo del Prado",
      description: "¡El Ratoncito adora las pinturas mágicas de este museo!",
      type: "museum",
      icon: createCustomIcon('🦷', '#7c3aed')
    },
    {
      id: 6,
      position: [40.4101, -3.6957],
      title: "Museo Reina Sofía",
      description: "Aquí el Ratoncito guarda sus tesoros más modernos",
      type: "museum",
      icon: createCustomIcon('🧀', '#7c3aed')
    },
    {
      id: 7,
      position: [40.4096, -3.6904],
      title: "Museo Thyssen",
      description: "La galería secreta del Ratoncito Pérez",
      type: "museum",
      icon: createCustomIcon('👑', '#7c3aed')
    }
  ];

  // Filtrar puntos según categoría activa
  const filteredPoints = activeFilter === 'all'
    ? pointsOfInterest
    : pointsOfInterest.filter(point => point.type === activeFilter);

  return (
    <div className="w-full h-screen pb-16 md:pb-0 relative">
      {/* Botón de filtros en la esquina superior derecha */}
      <div className="absolute top-[1.25rem] right-3 z-[1000] group">
        <button
          onClick={() => setShowFilterModal(true)}
          className="p-2 bg-gradient-to-r from-orange-400 to-orange-500 hover:from-orange-500 hover:to-orange-600 rounded-full shadow-lg transition-all duration-300 relative flex items-center justify-center transform hover:scale-105"
          aria-label="Mostrar filtros"
        >
          <svg className="w-5 h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M3 4a1 1 0 011-1h16a1 1 0 011 1v2.586a1 1 0 01-.293.707l-6.414 6.414a1 1 0 00-.293.707V17l-4 4v-6.586a1 1 0 00-.293-.707L3.293 7.293A1 1 0 013 6.586V4z" />
          </svg>
          <span className="absolute right-full mr-3 bg-white px-3 py-1.5 rounded-lg text-sm text-gray-700 opacity-0 group-hover:opacity-100 transition-opacity whitespace-nowrap shadow-md font-medium">
            Explora los puntos de interés
          </span>
        </button>
      </div>

      {/* Modal de filtros */}
      {showFilterModal && (
        <div className="fixed inset-0 bg-black/50 z-[1002] flex items-start justify-center px-4">
          <div className="bg-white rounded-xl p-6 w-full max-w-md mt-20 shadow-xl">
            <FilterModal
              isOpen={showFilterModal}
              onClose={() => setShowFilterModal(false)}
              categories={categories}
              activeFilter={activeFilter}
              setActiveFilter={setActiveFilter}
              filteredPoints={filteredPoints}
            />
          </div>
        </div>
      )}

      {/* Prompt de ubicación */}
      {showLocationPrompt && !permissionsGranted && (
        <div className="fixed inset-0 flex items-center justify-center z-[1001] bg-black/20 px-4 py-16 md:py-0">
          <ModalPermission
            onLocationGranted={(location) => {
              console.log("Ubicación recibida:", location);
              const newLocation = [location.latitude, location.longitude];
              setUserLocation(newLocation);

              setPermissionsGranted(true);
              setShowLocationPrompt(false);
            }}
          />
        </div>
      )}

      {/* Botón externo para ir a tu ubicación */}
      <div className="absolute bottom-20 right-3 z-[1000]">
        <button
          onClick={() => {
            if (map && userLocation) {
              map.flyTo(userLocation, 14);
            }
          }}
          className="p-3 bg-blue-500 text-white rounded-full shadow-lg hover:bg-blue-600 transition"
        >
          📍 Centrar
        </button>
      </div>

      {/* Mapa */}
      <MapContainer
        center={userLocation || madridPosition}
        zoom={14}
        style={{ height: '100%', width: '100%' }}
        zoomControl={false}
      >
        {userLocation && (
          <LocationMarker position={[userLocation[0], userLocation[1]]} />
        )}

        {/* Exponemos el mapa al padre */}
        <MapController onMapReady={setMap} />

        <LayersControl position="topleft" className="!z-[1000] !ml-4 !mt-24">
          <LayersControl.BaseLayer checked name="🗺️ Mapa limpio">
            <TileLayer
              url="https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png"
              attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors &copy; <a href="https://carto.com/attributions">CARTO</a>'
            />
          </LayersControl.BaseLayer>
          <LayersControl.BaseLayer name="🗺️ Mapa estándar">
            <TileLayer
              url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
              attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
            />
          </LayersControl.BaseLayer>
          <LayersControl.BaseLayer name="🛰️ Vista satélite">
            <TileLayer
              url="https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}"
              attribution='&copy; <a href="https://www.arcgis.com/">ArcGIS</a>'
            />
          </LayersControl.BaseLayer>
        </LayersControl>

        <ZoomControl position="bottomright" />

        {filteredPoints.map((point) => (
          <Marker
            key={point.id}
            position={point.position}
            icon={point.icon}
          >
            <Popup>
              <div className="text-center min-w-[200px]">
                <h4 className="font-bold text-lg mb-2" style={{ fontFamily: 'Quicksand, sans-serif' }}>{point.title}</h4>
                <p className="text-sm mb-4" style={{ fontFamily: 'Quicksand, sans-serif' }}>{point.description}</p>
                <div className="flex flex-col gap-3">
                  <span
                    className="text-xs px-3 py-1 rounded-full text-white self-center"
                    style={{ backgroundColor: categories.find(c => c.id === point.type)?.color }}
                  >
                    {categories.find(c => c.id === point.type)?.name}
                  </span>
                  <a
                    href={`https://www.google.com/maps/dir/?api=1&destination=${point.position[0]},${point.position[1]}`}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="mt-2 px-4 py-2 bg-gradient-to-r from-orange-400 to-orange-500 text-white rounded-full font-medium shadow-md hover:from-orange-500 hover:to-orange-600 transform hover:scale-105 transition-all flex items-center justify-center gap-2"
                    style={{ fontFamily: 'Quicksand, sans-serif' }}
                  >
                    <span>¡Vamos allá!</span>
                    <span>🚀</span>
                  </a>
                </div>
              </div>
            </Popup>
          </Marker>
        ))}
      </MapContainer>
    </div>
  );
};

export default MapView;

import React from 'react';

const LocationPermission = ({ onLocationGranted }) => {
  const handleLocationPermission = () => {
    if (navigator.geolocation) {
      navigator.geolocation.getCurrentPosition(
        (position) => {
          onLocationGranted({
            latitude: position.coords.latitude,
            longitude: position.coords.longitude
          });
        },
        (error) => {
          console.error('Error obteniendo la ubicación:', error);
          // En caso de error, usar coordenadas de Madrid como fallback
          onLocationGranted({
            latitude: 40.4168,
            longitude: -3.7038
          });
        }
      );
    } else {
      console.error('Geolocalización no soportada');
      // Si no hay soporte, usar coordenadas de Madrid como fallback
      onLocationGranted({
        latitude: 40.4168,
        longitude: -3.7038
      });
    }
  };

  return (
    <div className="bg-white p-4 md:p-6 rounded-2xl shadow-xl max-w-md w-[90%] text-center mx-4 my-auto mb-20 md:mb-0">
      <div className="mb-3 md:mb-6 text-4xl md:text-5xl animate-bounce">📍</div>
      <h2 className="text-xl md:text-2xl font-bold mb-4" style={{ fontFamily: 'Quicksand, sans-serif' }}>
        ¡Vamos a explorar Madrid!
      </h2>
      <p className="text-gray-600 mb-6 text-sm md:text-base px-2 md:px-6" style={{ fontFamily: 'Quicksand, sans-serif' }}>
        Para mostrarte los lugares más cercanos y guiarte mejor, necesito saber dónde estás.
      </p>
      <button
        onClick={handleLocationPermission}
        className="px-4 py-2 md:px-6 md:py-3 bg-gradient-to-r from-orange-400 to-orange-500 text-white font-semibold rounded-xl cursor-pointer text-base md:text-lg hover:from-orange-500 hover:to-orange-600 transition-all transform hover:scale-105 shadow-lg w-auto inline-flex items-center justify-center gap-2"
        style={{ fontFamily: 'Quicksand, sans-serif' }}
      >
        <span>Permitir ubicación</span>
        <span className="text-xl"></span>
      </button>
    </div>
  );
};

export default LocationPermission;

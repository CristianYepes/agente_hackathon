import React, { useState, useEffect } from 'react';
import {
    LocationPermissionState,
    checkPermissionState,
    pedirPermisos,
    iniciarGeolocalizacion
} from '../handlers/location';

const LocationPermission = ({ onLocationGranted }) => {
    const [permissionState, setPermissionState] = useState(LocationPermissionState.PROMPT);
    const [error, setError] = useState(null);
    const [location, setLocation] = useState(null);

    useEffect(() => {
        // Verificar el estado inicial de los permisos
        checkPermissionState().then(setPermissionState);
    }, []);

    const handleRequestPermission = async () => {
        try {
            setError(null);
            const result = await pedirPermisos();
            setPermissionState(result.state);
            setLocation(result.position);

            if (result.state === LocationPermissionState.GRANTED) {
                // Iniciar seguimiento de ubicación
                const stopTracking = iniciarGeolocalizacion(
                    (newLocation) => {
                        setLocation(newLocation);
                        if (onLocationGranted) onLocationGranted(newLocation);
                    },
                    (error) => setError(error.message)
                );

                // Limpiar el tracking cuando el componente se desmonte
                return () => {
                    if (stopTracking) stopTracking();
                };
            }
        } catch (err) {
            setError(err.message);
        }
    };

    const renderContent = () => {
        switch (permissionState) {
            case LocationPermissionState.PROMPT:
                return (
                    <div className="bg-blue-100 p-4 rounded-lg shadow">
                        <h3 className="text-lg font-semibold mb-2">Acceso a ubicación</h3>
                        <p className="mb-4">Necesitamos acceder a tu ubicación para mostrarte el mapa y sus funcionalidades.</p>
                        <button
                            onClick={handleRequestPermission}
                            className="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600 transition-colors"
                        >
                            Permitir acceso
                        </button>
                    </div>
                );

            case LocationPermissionState.DENIED:
                return (
                    <div className="bg-red-100 p-4 rounded-lg shadow">
                        <h3 className="text-lg font-semibold mb-2">Acceso denegado</h3>
                        <p className="mb-4">
                            Has denegado el acceso a tu ubicación. Para usar esta función,
                            necesitas permitir el acceso en la configuración de tu navegador.
                        </p>
                        <button
                            onClick={handleRequestPermission}
                            className="bg-red-500 text-white px-4 py-2 rounded hover:bg-red-600 transition-colors"
                        >
                            Intentar de nuevo
                        </button>
                    </div>
                );

            case LocationPermissionState.GRANTED:
                return (
                    <div className="bg-green-100 p-4 rounded-lg shadow">
                        <h3 className="text-lg font-semibold mb-2">Ubicación activada</h3>
                        {location && (
                            <p className="text-sm text-gray-600">
                                Lat: {location.latitude.toFixed(6)},
                                Lon: {location.longitude.toFixed(6)}
                            </p>
                        )}
                    </div>
                );

            case LocationPermissionState.UNAVAILABLE:
                return (
                    <div className="bg-yellow-100 p-4 rounded-lg shadow">
                        <h3 className="text-lg font-semibold mb-2">Ubicación no disponible</h3>
                        <p>Tu dispositivo no soporta o no tiene activada la geolocalización.</p>
                    </div>
                );

            default:
                return null;
        }
    };

    return (
        <div className="location-permission">
            {renderContent()}
            {error && (
                <div className="mt-4 p-3 bg-red-100 text-red-700 rounded">
                    {error}
                </div>
            )}
        </div>
    );
};

export default LocationPermission;

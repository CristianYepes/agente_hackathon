// Estados de los permisos de ubicación
export const LocationPermissionState = {
  PROMPT: 'prompt',      // Usuario aún no ha decidido
  GRANTED: 'granted',    // Permisos concedidos
  DENIED: 'denied',      // Permisos denegados
  UNAVAILABLE: 'unavailable', // Geolocalización no disponible
  ERROR: 'error'        // Error al solicitar permisos
};

// Comprueba si la geolocalización está disponible
export function isGeolocationAvailable() {
  return "geolocation" in navigator;
}

// Comprueba el estado actual de los permisos
export function checkPermissionState() {
  return new Promise((resolve) => {
    if (!isGeolocationAvailable()) {
      resolve(LocationPermissionState.UNAVAILABLE);
      return;
    }

    navigator.geolocation.getCurrentPosition(
      () => resolve(LocationPermissionState.GRANTED),
      (error) => {
        switch(error.code) {
          case error.PERMISSION_DENIED:
            resolve(LocationPermissionState.DENIED);
            break;
          case error.POSITION_UNAVAILABLE:
            resolve(LocationPermissionState.UNAVAILABLE);
            break;
          default:
            resolve(LocationPermissionState.ERROR);
        }
      },
      { timeout: 5000 }
    );
  });
}

// Solicita permisos de ubicación con manejo de errores detallado
export async function pedirPermisos() {
  if (!isGeolocationAvailable()) {
    throw new Error("La geolocalización no está disponible en este dispositivo");
  }

  try {
    const position = await new Promise((resolve, reject) => {
      navigator.geolocation.getCurrentPosition(
        resolve,
        reject,
        {
          enableHighAccuracy: true,
          timeout: 10000,
          maximumAge: 0
        }
      );
    });

    return {
      state: LocationPermissionState.GRANTED,
      position: {
        latitude: position.coords.latitude,
        longitude: position.coords.longitude,
        accuracy: position.coords.accuracy
      }
    };
  } catch (error) {
    let state;
    let message;

    switch(error.code) {
      case error.PERMISSION_DENIED:
        state = LocationPermissionState.DENIED;
        message = "Has denegado el acceso a tu ubicación. Para usar esta función, necesitamos que habilites los permisos en la configuración de tu navegador.";
        break;
      case error.POSITION_UNAVAILABLE:
        state = LocationPermissionState.UNAVAILABLE;
        message = "No podemos obtener tu ubicación actual. Por favor, verifica tu conexión GPS o internet.";
        break;
      case error.TIMEOUT:
        state = LocationPermissionState.ERROR;
        message = "Se agotó el tiempo para obtener tu ubicación. Por favor, inténtalo de nuevo.";
        break;
      default:
        state = LocationPermissionState.ERROR;
        message = "Ocurrió un error al obtener tu ubicación.";
    }

    throw new Error(message);
  }
}

// Función para iniciar el tracking de ubicación mientras la app esté abierta
export function iniciarGeolocalizacion(onActualizarPos, onError) {
  if (!isGeolocationAvailable()) {
    const error = new Error("Geolocalización no soportada en este navegador");
    if (onError) onError(error);
    return null;
  }

  const watcher = navigator.geolocation.watchPosition(
    position => {
      const locationData = {
        latitude: position.coords.latitude,
        longitude: position.coords.longitude,
        accuracy: position.coords.accuracy,
        timestamp: position.timestamp
      };
      
      if (onActualizarPos) onActualizarPos(locationData);
    },
    error => {
      if (onError) {
        let message;
        switch(error.code) {
          case error.PERMISSION_DENIED:
            message = "Acceso a ubicación denegado. Por favor, habilita los permisos.";
            break;
          case error.POSITION_UNAVAILABLE:
            message = "Ubicación no disponible. Verifica tu GPS o conexión.";
            break;
          case error.TIMEOUT:
            message = "Tiempo de espera agotado al obtener ubicación.";
            break;
          default:
            message = "Error al rastrear ubicación.";
        }
        onError(new Error(message));
      }
    },
    {
      enableHighAccuracy: false, // usamos precisión estándar para evitar timeouts
      maximumAge: 10000,        // permitimos datos de hasta 10s de antigüedad
      timeout: 30000            // aumentamos el timeout a 30s
    }
  );

  // Devuelve la función para parar el watcher
  return () => {
    if (watcher !== null) {
      navigator.geolocation.clearWatch(watcher);
    }
  };
}

import React, { useState } from 'react';

const OnboardingHeader = () => (
  <div className="fixed top-0 left-0 right-0 bg-gradient-to-r from-blue-500 to-purple-600 text-white py-3 px-4 flex items-center justify-center z-[1003]">
    <div className="flex items-center gap-3">
      <div className="w-10 h-10 bg-white rounded-full flex items-center justify-center">
        <span role="img" aria-label="ratón" className="text-2xl">🐭</span>
      </div>
      <div className="text-center">
        <h1 className="font-bold text-xl">Ratoncito Pérez</h1>
        <p className="text-sm text-white/90">Tu guía mágico de Madrid</p>
      </div>
    </div>
  </div>
);

const OnboardingModal = ({ onClose }) => {
  const [currentStep, setCurrentStep] = useState(1);
  const [expertiseLevel, setExpertiseLevel] = useState(null);
  const [childrenCount, setChildrenCount] = useState(0);
  const [childrenAges, setChildrenAges] = useState([]);
  const [isTransitioning, setIsTransitioning] = useState(false);
  const [errors, setErrors] = useState({
    adventure: false,
    children: false,
    ages: false
  });

  const steps = [
    {
      title: '¡Hola! Soy el Ratoncito Pérez',
      content: '¡Bienvenidos a una aventura mágica por Madrid! Juntos descubriremos los secretos más fascinantes de la ciudad.'
    },
    {
      title: '¿Cuántos niños vienen de aventura?',
      content: (
        <div className="space-y-8">
          <div>
            <p className="text-gray-600 mb-4 text-center">Primero, selecciona el número de niños:</p>
            <div className="grid grid-cols-2 gap-4">
              <button
                onClick={() => {
                  setChildrenCount(1);
                  setErrors(prev => ({ ...prev, children: false }));
                }}
                className={`p-6 rounded-xl transition-all transform hover:scale-105 ${
                  childrenCount === 1
                    ? 'bg-gradient-to-r from-orange-400 to-orange-500 text-white shadow-lg'
                    : 'bg-white border-2 border-orange-200 hover:border-orange-400'
                }`}
              >
                <h3 className="font-bold text-lg">1 Niño</h3>
              </button>

              <button
                onClick={() => {
                  setChildrenCount(2);
                  setErrors(prev => ({ ...prev, children: false }));
                }}
                className={`p-6 rounded-xl transition-all transform hover:scale-105 ${
                  childrenCount >= 2
                    ? 'bg-gradient-to-r from-orange-400 to-orange-500 text-white shadow-lg'
                    : 'bg-white border-2 border-orange-200 hover:border-orange-400'
                }`}
              >
                <h3 className="font-bold text-lg">2 o más niños</h3>
              </button>
            </div>
            {errors.children && (
              <p className="text-red-500 text-sm mt-3 animate-bounce text-center">Por favor, indica cuántos niños vienen de aventura</p>
            )}
          </div>

          <div className="mt-8">
            <p className="text-gray-600 mb-4 text-center">Ahora, selecciona el rango de edad:</p>
            <div className="grid grid-cols-3 gap-3">
              <button
                onClick={() => {
                  setChildrenAges(['5-8']);
                  setErrors(prev => ({ ...prev, ages: false }));
                }}
                className={`p-4 rounded-xl transition-all ${
                  childrenAges.includes('5-8')
                    ? 'bg-gradient-to-r from-orange-400 to-orange-500 text-white shadow-lg'
                    : 'bg-white border-2 border-orange-200 hover:border-orange-400'
                }`}
              >
                <span className="font-bold">5-8</span>
                <br />
                años
              </button>
              <button
                onClick={() => {
                  setChildrenAges(['8-12']);
                  setErrors(prev => ({ ...prev, ages: false }));
                }}
                className={`p-4 rounded-xl transition-all ${
                  childrenAges.includes('8-12')
                    ? 'bg-gradient-to-r from-orange-400 to-orange-500 text-white shadow-lg'
                    : 'bg-white border-2 border-orange-200 hover:border-orange-400'
                }`}
              >
                <span className="font-bold">8-12</span>
                <br />
                años
              </button>
              <button
                onClick={() => {
                  setChildrenAges(['12-15']);
                  setErrors(prev => ({ ...prev, ages: false }));
                }}
                className={`p-4 rounded-xl transition-all ${
                  childrenAges.includes('12-15')
                    ? 'bg-gradient-to-r from-orange-400 to-orange-500 text-white shadow-lg'
                    : 'bg-white border-2 border-orange-200 hover:border-orange-400'
                }`}
              >
                <span className="font-bold">12-15</span>
                <br />
                años
              </button>
            </div>
            {errors.ages && (
              <p className="text-red-500 text-sm mt-3 animate-bounce text-center">Por favor, selecciona un rango de edad</p>
            )}
          </div>
        </div>
      )
    },
    {
      title: '¡Hola, familia! ¿Qué tipo de aventura buscáis hoy?',
      content: (
        <div className="space-y-6">
          <div className="grid grid-cols-1 gap-4">
            <button
              onClick={() => {
                setExpertiseLevel('basic');
                setErrors(prev => ({ ...prev, adventure: false }));
                localStorage.setItem('adventureType', 'basic');
              }}
              className={`p-4 md:p-5 rounded-xl transition-all transform hover:scale-105 text-left ${
                expertiseLevel === 'basic' 
                  ? 'bg-gradient-to-r from-orange-400 to-orange-500 text-white shadow-lg' 
                  : 'bg-white border-2 border-orange-200 hover:border-orange-400'
              }`}
            >
              <div className="flex items-start gap-3">
                <span className="text-xl md:text-2xl">🎭</span>
                <div>
                  <h3 className="font-bold text-base md:text-lg mb-1 md:mb-2" style={{ fontFamily: 'Quicksand, sans-serif' }}>Aventura Mágica</h3>
                  <p className="text-xs md:text-sm opacity-90" style={{ fontFamily: 'Quicksand, sans-serif' }}>Un viaje lleno de leyendas, diversión y juegos por Madrid. ¡Perfecto para toda la familia!</p>
                </div>
              </div>
            </button>

            <button
              onClick={() => {
                setExpertiseLevel('expert');
                setErrors(prev => ({ ...prev, adventure: false }));
                localStorage.setItem('adventureType', 'expert');
              }}
              className={`p-4 md:p-5 rounded-xl transition-all transform hover:scale-105 text-left ${
                expertiseLevel === 'expert' 
                  ? 'bg-gradient-to-r from-orange-400 to-orange-500 text-white shadow-lg' 
                  : 'bg-white border-2 border-orange-200 hover:border-orange-400'
              }`}
            >
              <div className="flex items-start gap-3">
                <span className="text-xl md:text-2xl">🏛️</span>
                <div>
                  <h3 className="font-bold text-base md:text-lg mb-1 md:mb-2" style={{ fontFamily: 'Quicksand, sans-serif' }}>Secretos de los Sabios</h3>
                  <p className="text-xs md:text-sm opacity-90" style={{ fontFamily: 'Quicksand, sans-serif' }}>Descubre la historia profunda, arquitectura y curiosidades fascinantes de Madrid.</p>
                </div>
              </div>
            </button>
          </div>
          {errors.adventure && (
            <p className="text-red-500 text-sm mt-4 animate-bounce text-center" style={{ fontFamily: 'Quicksand, sans-serif' }}>
              Por favor, selecciona un tipo de aventura para continuar
            </p>
          )}
        </div>
      )
    },

  ];

  const validateStep = () => {
    switch(currentStep) {
      case 1:
        return true; // Paso informativo
      case 2:
        // Validación de número de niños y edades
        if (childrenCount === 0) {
          setErrors(prev => ({
            ...prev,
            children: true
          }));
          return false;
        }
        if (childrenAges.length === 0) {
          setErrors(prev => ({
            ...prev,
            ages: true
          }));
          return false;
        }
        return true;
      case 3:
        if (!expertiseLevel) {
          setErrors(prev => ({
            ...prev,
            adventure: true
          }));
          return false;
        }
        return true;
      default:
        return true;
    }
  };

  const handleNext = () => {
    if (!validateStep()) {
      return;
    }
    
    // Si estamos en el último paso y todo está validado, cerramos el modal
    if (currentStep === steps.length) {
      setIsTransitioning(true);
      setTimeout(() => {
        onClose();
      }, 500);
      return;
    }
    
    // Iniciar la transición
    setIsTransitioning(true);
    
    // Esperar a que termine la transición antes de cambiar el contenido
    setTimeout(() => {
      setCurrentStep(currentStep + 1);
      // Limpiar los errores al avanzar
      setErrors({
        children: false,
        age: false,
        adventure: false
      });
      // Restaurar la visibilidad después del cambio de contenido
      setTimeout(() => {
        setIsTransitioning(false);
      }, 50);
    }, 300);
  };

  return (
    <div className="fixed inset-0 bg-gradient-to-br from-orange-100 to-orange-200 flex justify-center items-center z-[1000] p-4">
      <div 
        className={`bg-white p-4 md:p-8 rounded-2xl max-w-lg w-full mx-auto text-center shadow-xl my-20 md:my-0 max-h-[calc(100vh-10rem)] overflow-y-auto transition-all duration-500 ease-out transform ${
          isTransitioning ? 'opacity-0 translate-y-4' : 'opacity-100 translate-y-0'
        }`}
      >
        <h2 
          className={`mb-4 md:mb-6 text-orange-500 text-xl md:text-2xl font-bold transition-all duration-300 ease-out transform ${
            isTransitioning ? 'opacity-0 -translate-y-4' : 'opacity-100 translate-y-0'
          }`} 
          style={{ fontFamily: 'Quicksand, sans-serif' }}
        >
          {steps[currentStep - 1].title}
        </h2>
        <div 
          className={`text-gray-700 mb-6 md:mb-8 transition-all duration-300 ease-out transform ${
            isTransitioning ? 'opacity-0 translate-y-4' : 'opacity-100 translate-y-0'
          }`} 
          style={{ fontFamily: 'Quicksand, sans-serif' }}
        >
          {steps[currentStep - 1].content}
        </div>

        <div className="flex flex-col items-center gap-4 mt-4 md:mt-8">
          <button
            onClick={handleNext}
            className={`px-8 py-3 bg-gradient-to-r from-orange-400 to-orange-500 text-white font-semibold rounded-xl text-lg hover:from-orange-500 hover:to-orange-600 transition-all transform hover:scale-105 shadow-lg w-full md:w-auto ${
              currentStep === steps.length && !expertiseLevel ? 'cursor-not-allowed' : 'cursor-pointer'
            }`}
            style={{ fontFamily: 'Quicksand, sans-serif' }}
          >
            {currentStep === steps.length 
              ? '¡Vamos a comenzar la aventura! 🚀'
              : 'Siguiente'
            }
          </button>
        </div>
      </div>
    </div>
  );
};

export default OnboardingModal;

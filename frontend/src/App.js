import { BrowserRouter as Router, Routes, Route, useNavigate, useLocation } from "react-router-dom"
import { useState, useEffect } from 'react';
import MapView from './components/MapView';
import ChatView from './components/ChatView';
import OnboardingModal from './components/OnboardingModal';
import MobileNavbar from './components/MobileNavbar';
import DesktopNavigation from './components/DesktopNavigation';
import WelcomeAnimation from './components/WelcomeAnimation';

// Componente para manejar la navegación
const AppContent = () => {
  const navigate = useNavigate();
  const location = useLocation();
  const [showWelcome, setShowWelcome] = useState(true);
  const [showOnboarding, setShowOnboarding] = useState(false);
  const [showContent, setShowContent] = useState(false);
  const [currentView, setCurrentView] = useState('chat');

  useEffect(() => {
    // Actualizar la vista actual basada en la ruta
    if (location.pathname === '/map') {
      setCurrentView('map');
    } else {
      setCurrentView('chat');
    }
  }, [location]);

  const handleViewChange = (view) => {
    if (view === 'map') {
      navigate('/map');
    } else {
      navigate('/');
    }
    setCurrentView(view);
  };

  return (
    <div className="w-screen h-screen overflow-hidden">
      {/* Header permanente */}
      <div className="fixed top-0 left-0 right-0 bg-gradient-to-r from-orange-400 to-orange-600 text-white py-4 px-4 flex items-center justify-center z-[1003]">
        <div className="flex items-center gap-4">
          <div className="w-12 h-12 bg-white rounded-full flex items-center justify-center shadow-lg animate-bounce" style={{ animationDuration: '2s' }}>
            <span role="img" aria-label="ratón" className="text-3xl transform hover:scale-110 transition-transform">🐭</span>
          </div>
          <div className="text-center">
            <h1 className="font-bold text-2xl" style={{ fontFamily: 'Quicksand, sans-serif' }}>Ratoncito Pérez</h1>
            <p className="text-sm text-white/95" style={{ fontFamily: 'Quicksand, sans-serif' }}>Tu guía mágico de Madrid</p>
          </div>
        </div>
      </div>

      {/* Contenido principal */}
      {showWelcome ? (
        <WelcomeAnimation onAnimationEnd={() => {
          setShowWelcome(false);
          setShowOnboarding(true);
        }} />
      ) : (
        <>
          {showOnboarding && (
            <OnboardingModal 
              onClose={() => {
                setShowOnboarding(false);
                setShowContent(true);
                navigate('/map');
              }} 
            />
          )}
          {showContent && (
            <div className="pt-20">
              <Routes>
                <Route path="/map" element={<MapView />} />
                <Route path="/" element={<ChatView />} />
              </Routes>
            </div>
          )}
        </>
      )}

      {/* Navegación - Solo visible cuando se completa el onboarding */}
      {showContent && (
        <>
          <DesktopNavigation currentView={currentView} onViewChange={handleViewChange} />
          <MobileNavbar currentView={currentView} onViewChange={handleViewChange} />
        </>
      )}
    </div>
  );
};

function App() {
  return (
    <Router>
      <AppContent />
    </Router>
  );
}

export default App;

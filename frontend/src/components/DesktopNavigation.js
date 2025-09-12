import React from 'react';

const DesktopNavigation = ({ currentView, onViewChange }) => {
  return (
    <div className="hidden md:flex fixed top-24 left-1/2 transform -translate-x-1/2 z-[1004] bg-white rounded-full shadow-xl p-1.5">
      <button
        onClick={() => onViewChange('map')}
        className={`px-8 py-3 rounded-full transition-all transform hover:scale-105 ${
          currentView === 'map'
            ? 'bg-gradient-to-r from-orange-400 to-orange-500 text-white shadow-md'
            : 'hover:bg-orange-50 text-gray-700'
        }`}
        style={{ fontFamily: 'Quicksand, sans-serif' }}
      >
        <div className="flex items-center gap-2">
          <span>🗺️</span>
          <span className="font-medium">Mapa</span>
        </div>
      </button>
      <button
        onClick={() => onViewChange('chat')}
        className={`px-8 py-3 rounded-full transition-all transform hover:scale-105 ${
          currentView === 'chat'
            ? 'bg-gradient-to-r from-orange-400 to-orange-500 text-white shadow-md'
            : 'hover:bg-orange-50 text-gray-700'
        }`}
        style={{ fontFamily: 'Quicksand, sans-serif' }}
      >
        <div className="flex items-center gap-2">
          <span>💬</span>
          <span className="font-medium">Chat</span>
        </div>
      </button>
    </div>
  );
};

export default DesktopNavigation;

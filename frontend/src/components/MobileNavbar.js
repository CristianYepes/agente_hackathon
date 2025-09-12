import React from 'react';

const MobileNavbar = ({ currentView, onViewChange }) => {
  return (
    <div className="fixed bottom-0 left-0 right-0 bg-white border-t border-gray-200 p-2 md:hidden z-[1002]">
      <div className="flex justify-around items-center">
        <button
          onClick={() => onViewChange('map')}
          className={`flex flex-col items-center p-2 rounded-lg ${
            currentView === 'map' ? 'text-orange-500 bg-orange-50' : 'text-gray-600'
          }`}
        >
          <svg
            xmlns="http://www.w3.org/2000/svg"
            className="h-6 w-6"
            fill="none"
            viewBox="0 0 24 24"
            stroke="currentColor"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth={2}
              d="M9 20l-5.447-2.724A1 1 0 013 16.382V5.618a1 1 0 011.447-.894L9 7m0 13l6-3m-6-3l-6-3m6-3l6-3m6 3v7.382a1 1 0 01-.553.894L15 17"
            />
          </svg>
          <span className="text-xs mt-1">Mapa</span>
        </button>

        <button
          onClick={() => onViewChange('chat')}
          className={`flex flex-col items-center p-2 rounded-lg ${
            currentView === 'chat' ? 'text-orange-500 bg-orange-50' : 'text-gray-600'
          }`}
        >
          <svg
            xmlns="http://www.w3.org/2000/svg"
            className="h-6 w-6"
            fill="none"
            viewBox="0 0 24 24"
            stroke="currentColor"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth={2}
              d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z"
            />
          </svg>
          <span className="text-xs mt-1">Chat</span>
        </button>
      </div>
    </div>
  );
};

export default MobileNavbar;

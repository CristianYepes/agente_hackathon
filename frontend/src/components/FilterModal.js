import React from 'react';

const FilterModal = ({ isOpen, onClose, categories, activeFilter, setActiveFilter, filteredPoints }) => {
  return (
    <>
      {/* Overlay */}
      <div 
        className={`fixed inset-0 bg-black bg-opacity-50 transition-opacity z-[1001] ${
          isOpen ? 'opacity-100' : 'opacity-0 pointer-events-none'
        }`}
        onClick={onClose}
      />

      {/* Modal */}
      <div 
        className={`fixed top-20 right-4 h-[calc(100vh-20rem)] w-80 max-w-[90vw] bg-white shadow-lg transform transition-transform z-[1002] overflow-y-auto rounded-xl ${
          isOpen ? 'translate-x-0' : 'translate-x-full'
        }`}
      >
        <div className="p-4">
          <div className="flex justify-between items-center mb-4">
            <h4 className="font-semibold">🔍 Filtrar por categoría</h4>
            <button 
              onClick={onClose}
              className="p-2 hover:bg-gray-100 rounded-full"
            >
              <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          </div>

          <div className="grid grid-cols-2 gap-2 mb-4">
            {categories.map((category) => (
              <button
                key={category.id}
                onClick={() => setActiveFilter(category.id)}
                className={`px-3 py-2 text-xs rounded transition-colors ${
                  activeFilter === category.id
                    ? 'bg-blue-500 text-white'
                    : 'bg-gray-100 hover:bg-gray-200 text-gray-700'
                }`}
              >
                <div className="flex items-center gap-2">
                  <div
                    className="w-3 h-3 rounded-full"
                    style={{ backgroundColor: category.color }}
                  ></div>
                  {category.name}
                </div>
              </button>
            ))}
          </div>

          <div>
            <h4 className="font-semibold mb-2">📍 Lugares ({filteredPoints.length}):</h4>
            <div className="space-y-2">
              {filteredPoints.map((point) => (
                <div
                  key={point.id}
                  className="p-3 border rounded hover:bg-gray-50 cursor-pointer"
                >
                  <div className="flex items-start gap-2">
                    <div
                      className="w-4 h-4 rounded-full mt-1 flex-shrink-0"
                      style={{ backgroundColor: categories.find(c => c.id === point.type)?.color }}
                    ></div>
                    <div>
                      <h5 className="font-semibold text-sm">{point.title}</h5>
                      <p className="text-xs text-gray-600 mt-1">{point.description}</p>
                      <span className="text-xs bg-gray-100 px-2 py-1 rounded mt-2 inline-block">
                        {categories.find(c => c.id === point.type)?.name}
                      </span>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>
    </>
  );
};

export default FilterModal;

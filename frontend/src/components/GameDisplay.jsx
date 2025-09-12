import React from 'react';

const GameDisplay = ({ game }) => {
  if (!game) return null;

  return (
    <div style={{ marginTop: '1rem', background: '#f0f8ff', color: '#040404ff', padding: '1rem', borderRadius: '8px' }}>
      <h3>🧙‍♂️ Tu juego mágico:</h3>
      <p>{game}</p>
    </div>
  );
};

export default GameDisplay;

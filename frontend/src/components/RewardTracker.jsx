import React from 'react';

const RewardTracker = ({ points }) => {
  return (
    <div style={{ marginTop: '1rem', background: '#e6ffe6', color: '#040404ff', padding: '1rem', borderRadius: '8px' }}>
      <h4>🪙 Tus recompensas mágicas:</h4>
      <p>Monedas mágicas acumuladas: <strong>{points}</strong></p>
      {points >= 3 && <p>🌟 ¡Has desbloqueado una insignia mágica del Ratoncito Pérez!</p>}
    </div>
  );
};

export default RewardTracker;

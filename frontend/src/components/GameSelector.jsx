import React, { useState } from 'react';
import GameEngine from './GameEngine';
import RewardTracker from './RewardTracker';

const GameSelector = () => {
  const [location, setLocation] = useState('');
  const [age, setAge] = useState('');
  const [rewards, setRewards] = useState(0);
  const [started, setStarted] = useState(false);

  const handleStart = () => {
    setStarted(true);
    setRewards(0); // Opcional: reinicia puntos al empezar
  };

  return (
    <div style={{ padding: '1rem' }}>
      <h2>🐭 Juegos del Ratoncito Pérez</h2>
      <label>
        Lugar:
        <select value={location} onChange={(e) => setLocation(e.target.value)}>
          <option value="">Selecciona un lugar</option>
          <option value="Palacio Real">Palacio Real</option>
          <option value="Museo del Prado">Museo del Prado</option>
          <option value="Puerta del Sol">Puerta del Sol</option>
          <option value="Plaza Mayor">Plaza Mayor</option>
          <option value="Parque del Retiro">Parque del Retiro</option>
          <option value="Museo Reina Sofía">Museo Reina Sofía</option>
          <option value="Museo Thyssen">Museo Thyssen</option>
        </select>
      </label>
      <br />
      <label>
        Edad del niño:
        <input
          type="number"
          value={age}
          onChange={(e) => setAge(e.target.value)}
          min="3"
          max="12"
        />
      </label>
      <br />
      {!started && location && age >= 3 && age <= 12 && (
        <button onClick={handleStart} style={{ marginTop: '1rem' }}>
          Empezar a jugar
        </button>
      )}
      {started && location && age && (
        <>
          <GameEngine location={location} age={parseInt(age)} onReward={() => setRewards(rewards + 1)} />
          <RewardTracker points={rewards} />
        </>
      )}
    </div>
  );
};

export default GameSelector;

import React, { useState } from 'react';
import { getGameTemplate } from './GameTemplates';


const GameEngine = ({ location, age, onReward }) => {
  const game = getGameTemplate(location, age);
  const [response, setResponse] = useState('');
  const [feedback, setFeedback] = useState('');
  const [agentReply, setAgentReply] = useState('');
  const [loading, setLoading] = useState(false);

  // Debug: mostrar agentReply en consola en cada render
  React.useEffect(() => {
    // eslint-disable-next-line no-console
    console.log('agentReply:', agentReply);
  }, [agentReply]);

  const handleSubmit = async () => {
    const validation = game.validate(response);
    if (validation === true) {
      setFeedback('🎉 ¡Correcto! Has ganado una moneda mágica.');
      onReward();
      setLoading(true);
      setAgentReply('');
      try {
        // Use REACT_APP_API_URL if provided, otherwise use a relative path so CRA's proxy can forward to backend in development
        const apiBase = process.env.REACT_APP_API_URL || '';
        const res = await fetch(`${apiBase}/game/crew-explain`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            topic: response, // respuesta del usuario
            age: parseInt(age),
            correct_answer: game.answer || '',
            selected_place: location,
            question: game.description || ''
          })
        });
        const data = await res.json();
        setAgentReply(data.reply);
      } catch (err) {
        // eslint-disable-next-line no-console
        console.error('Error contacting backend:', err);
        setAgentReply('No se pudo obtener respuesta educativa.');
      }
      setLoading(false);
    } else if (validation === 'not-in-prado') {
      setFeedback('No niño no, esos cuadros no se encuentran en el Museo del Prado');
      setAgentReply('');
    } else {
      setFeedback('🔍 Sigue buscando... ¡tú puedes!');
      setAgentReply('');
    }
  };

  return (
    <div style={{ marginTop: '1rem', background: '#fff8dc', color: '#040404ff', padding: '1rem', borderRadius: '8px' }}>
      <h3>{game.title}</h3>
      <p>{game.description}</p>
      {game.type === 'choice' && game.options && (
        <div style={{ margin: '1rem 0' }}>
          {game.options.map((opt) => (
            <button
              key={opt}
              style={{ margin: '0.25rem', padding: '0.5rem 1rem', background: response === opt ? '#b2dfdb' : '#fff' }}
              onClick={() => setResponse(opt)}
              disabled={!!response && feedback === ''}
            >
              {opt}
            </button>
          ))}
          {response && (
            <div style={{ marginTop: '1rem' }}>
              <button onClick={handleSubmit}>Enviar respuesta</button>
              {(feedback && feedback !== '🎉 ¡Correcto! Has ganado una moneda mágica.') && (
                <button style={{ marginLeft: '1rem' }} onClick={() => { setResponse(''); setFeedback(''); setAgentReply(''); }}>Elegir otra respuesta</button>
              )}
            </div>
          )}
        </div>
      )}
      {game.type === 'yesno' && (
        <>
          <button onClick={() => setResponse('yes')}>¡Sí!</button>
          <button onClick={() => setResponse('no')}>No</button>
        </>
      )}
      {game.type === 'text' && (
        <>
          <input
            type="text"
            value={response}
            onChange={(e) => setResponse(e.target.value)}
            placeholder="Escribe tu respuesta..."
          />
          <button onClick={handleSubmit}>Enviar</button>
        </>
      )}
      {response && game.type === 'yesno' && <button onClick={handleSubmit}>Enviar respuesta</button>}
      <p>{feedback}</p>
      {loading && <p>El Ratoncito Pérez está pensando...</p>}
      {(agentReply && (typeof agentReply === 'string' ? agentReply.trim() !== '' : true)) && (
        <div style={{ marginTop: '1rem', background: '#e0f7fa', padding: '0.5rem', borderRadius: '6px' }}>
          <strong>Ratoncito dice:</strong> {agentReply}
        </div>
      )}
    </div>
  );
};

export default GameEngine;

export function getGameTemplate(location, age) {
  if (age < 6) {
    return games3to5[location] || defaultGame;
  } else if (age <= 9) {
    return games6to9[location] || defaultGame;
  } else {
    return games10to12[location] || defaultGame;
  }
}

const defaultGame = {
  title: 'Juego no disponible',
  description: 'Este lugar aún no tiene juegos mágicos.',
  type: 'text',
  validate: () => false
};

const games3to5 = {
  'Museo del Prado': {
    title: '🎨 Colores y Caritas',
    description: '¿Cuál de estos cuadros tiene una cara sonriente y muchos colores?',
    type: 'choice',
    options: ['Las Meninas', 'El Jardín de las Delicias', 'La Maja Desnuda'],
    answer: 'El Jardín de las Delicias',
    validate: (res) => res === 'El Jardín de las Delicias'
  },
  'Palacio Real': {
    title: '🔍 Busca el Tesoro Real',
    description: '¿Qué objeto dorado es el más famoso del Palacio Real?',
    type: 'choice',
    options: ['La Corona', 'La Espada', 'El Escudo'],
    answer: 'La Corona',
    validate: (res) => res === 'La Corona'
  },
  'Puerta del Sol': {
    title: '⏰ Salta y Cuenta',
    description: '¿Cuántos relojes puedes ver en la plaza?',
    type: 'text',
    validate: (res) => !isNaN(Number(res)) && Number(res) > 0
  },
  'Plaza Mayor': {
    title: '� Cuenta los arcos',
    description: '¿Cuántos arcos tiene la Plaza Mayor?',
    type: 'text',
    validate: (res) => !isNaN(Number(res)) && Number(res) > 0
  },
  'Parque del Retiro': {
    title: '🦆 Patos en el estanque',
    description: '¿Cuántos patos ves en el estanque?',
    type: 'text',
    validate: (res) => !isNaN(Number(res)) && Number(res) >= 0
  },
  'Museo Reina Sofía': {
    title: '🎨 Colores en el Guernica',
    description: '¿Cuántos colores diferentes ves en el Guernica?',
    type: 'text',
    validate: (res) => !isNaN(Number(res)) && Number(res) > 0
  },
  'Museo Thyssen': {
    title: '🦁 Animales en el Thyssen',
    description: '¿Puedes nombrar un animal que veas en un cuadro?',
    type: 'text',
    validate: (res) => typeof res === 'string' && res.length > 0
  }
};

const games6to9 = {
  'Museo del Prado': {
    title: '🖼️ El Cuadro Encantado',
    description: '¿Cuál de estos cuadros has encontrado en El Museo Del Prado?',
    type: 'choice',
    options: ['Las Meninas', 'La Noche Estrellada', 'La Gioconda'],
    answer: 'Las Meninas',
    validate: (res) => {
      if (res === 'Las Meninas') return true;
      if (res === 'La Noche Estrellada' || res === 'La Gioconda') return 'not-in-prado';
      return false;
    }
  },
  'Palacio Real': {
    title: '🕵️ Detectives del Palacio',
    description: '¿Cuántos peldaños tiene la escalera principal?',
    type: 'choice',
    options: ['10', '12', '15'],
    answer: '10',
    validate: (res) => res === '10'
  },
  'Puerta del Sol': {
    title: '🎤 Entrevista en Sol',
    description: 'Haz una mini entrevista a un familiar: ¿qué es lo que más le gusta de la plaza?',
    type: 'text',
    validate: (res) => typeof res === 'string' && res.length > 0
  },
  'Plaza Mayor': {
    title: 'Búsqueda del Tesoro',
    description: 'Encuentra un escudo en una fachada y descríbelo.',
    type: 'text',
    validate: (res) => typeof res === 'string' && res.length > 0
  },
  'Parque del Retiro': {
    title: '🗺️ Mini gymkana',
    description: 'Encuentra una estatua, una fuente y una flor.',
    type: 'text',
    validate: (res) => typeof res === 'string' && res.length > 0
  },
  'Museo Reina Sofía': {
    title: '🖼️ Obra moderna',
    description: 'Elige una obra moderna y explica qué te hace sentir.',
    type: 'text',
    validate: (res) => typeof res === 'string' && res.length > 0
  },
  'Museo Thyssen': {
    title: '🎨 Dibuja tu favorito',
    description: 'Elige tu cuadro favorito y haz un dibujo rápido.',
    type: 'text',
    validate: (res) => typeof res === 'string' && res.length > 0
  }
};

const games10to12 = {
  'Museo del Prado': {
    title: '🎓 Misión Art Masters',
    description: '¿Cuál de estos cuadros fue pintado por Velázquez?',
    type: 'choice',
    options: ['Las Meninas', 'El Jardín de las Delicias', 'La Maja Desnuda'],
    answer: 'Las Meninas',
    validate: (res) => res === 'Las Meninas'
  },
  'Palacio Real': {
    title: '🧩 Escape Real',
    description: '¿Cuál es la mejor estrategia para escapar del Palacio Real sin ser visto?',
    type: 'choice',
    options: ['Disfrazarse', 'Esconderse', 'Correr rápido'],
    answer: 'Disfrazarse',
    validate: (res) => res === 'Disfrazarse'
  },
  'Puerta del Sol': {
    title: '📚 Historia de Sol',
    description: 'Investiga por qué la Puerta del Sol es tan famosa y cuéntalo.',
    type: 'text',
    validate: (res) => typeof res === 'string' && res.length > 10
  },
  'Plaza Mayor': {
    title: '� Historia de la Plaza',
    description: 'Investiga la historia de la Plaza Mayor y compártela.',
    type: 'text',
    validate: (res) => typeof res === 'string' && res.length > 10
  },
  'Parque del Retiro': {
    title: '📚 Origen del Retiro',
    description: 'Investiga el origen del parque y cuéntalo.',
    type: 'text',
    validate: (res) => typeof res === 'string' && res.length > 10
  },
  'Museo Reina Sofía': {
    title: '📚 Historia del Guernica',
    description: 'Investiga la historia del Guernica y resúmela.',
    type: 'text',
    validate: (res) => typeof res === 'string' && res.length > 10
  },
  'Museo Thyssen': {
    title: '📚 Obra impresionista',
    description: 'Investiga la historia de una obra impresionista.',
    type: 'text',
    validate: (res) => typeof res === 'string' && res.length > 10
  }
};

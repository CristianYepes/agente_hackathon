export function generateGame(location, age) {
  if (!location || isNaN(age)) return "Por favor, selecciona un lugar y una edad válida.";

  // Juegos por ubicación y edad
  const games = {
    "Palacio Real": {
      5: [
        "🔍 Busca la corona escondida en la sala del trono.",
        "🤴 Imita la pose de un guardia real sin reírte.",
        "🏰 Cuenta cuántas ventanas ves desde la plaza."
      ],
      8: [
        "✏️ Haz un dibujo rápido del Palacio en 2 minutos.",
        "👑 Inventa una historia sobre un rey travieso.",
        "🛡️ Busca un escudo real y descríbelo."
      ],
      12: [
        "📚 Investiga qué rey vivió aquí y cuéntalo en 1 minuto.",
        "📸 Haz una foto creativa imitando una estatua.",
        "🔎 Encuentra un detalle arquitectónico curioso y explícalo."
      ]
    },
    "Museo del Prado": {
      5: [
        "🎨 Busca un cuadro con animales y nómbralos.",
        "😄 Imita la cara de un personaje de un cuadro.",
        "🌈 Cuenta cuántos colores diferentes ves en una pintura."
      ],
      8: [
        "🖼️ Elige tu cuadro favorito y explica por qué.",
        "✏️ Haz un retrato rápido de tu acompañante.",
        "� Inventa un diálogo entre dos personajes de un cuadro."
      ],
      12: [
        "📚 Investiga la historia de una obra famosa y resúmela.",
        "😂 Crea un meme con una pintura clásica.",
        "🖌️ Encuentra una obra de Goya y describe su estilo."
      ]
    },
    "Puerta del Sol": {
      5: [
        "🦶 Salta en un pie hasta el centro de la plaza (kilómetro 0).",
        "⏰ Cuenta cuántos relojes ves alrededor.",
        "🤪 Haz una foto haciendo una cara divertida junto al cartel de Tío Pepe."
      ],
      8: [
        "👋 Inventa un saludo especial para la Puerta del Sol y enséñaselo a alguien.",
        "🎤 Haz una mini entrevista a un familiar: ¿qué es lo que más le gusta de la plaza?",
        "🔍 Busca una placa curiosa y copia lo que pone."
      ],
      12: [
        "� Investiga por qué la Puerta del Sol es tan famosa y cuéntalo en 2 minutos.",
        "🤳 Haz un reto de selfies: 3 fotos con diferentes monumentos de la plaza.",
        "🧭 Crea un reto de orientación: ¿puedes señalar hacia el norte sin mirar el móvil?"
      ]
    },
    "Plaza Mayor": {
      5: [
        "🔢 Cuenta cuántos arcos tiene la plaza.",
        "🕴️ Imita a un estatua humana que veas en la plaza.",
        "✏️ Haz un dibujo rápido de la estatua de Felipe III."
      ],
      8: [
        "📜 Inventa una historia sobre un mercado antiguo en la plaza.",
        "�️ Haz una búsqueda del tesoro: encuentra un escudo en una fachada.",
        "❓ Pregunta a alguien qué evento famoso ocurre aquí cada año."
      ],
      12: [
        "📚 Investiga la historia de la Plaza Mayor y compártela.",
        "📸 Haz una foto artística de los balcones.",
        "🔎 Crea un reto: ¿puedes encontrar una placa con una fecha antigua?"
      ]
    },
    "Parque del Retiro": {
      5: [
        "🦆 Cuenta cuántos patos ves en el estanque.",
        "🏃 Haz una carrera de velocidad con un amigo hasta un árbol.",
        "🐦 Imita el sonido de 3 animales que puedas ver o imaginar en el parque."
      ],
      8: [
        "�️ Haz una mini gymkana: encuentra una estatua, una fuente y una flor.",
        "🧚 Inventa una historia sobre un duende que vive en el Retiro.",
        "🤸 Haz una foto saltando delante del Palacio de Cristal."
      ],
      12: [
        "📚 Investiga el origen del parque y cuéntalo.",
        "🧭 Haz un reto de orientación: encuentra el árbol más grande que veas.",
        "✍️ Crea un poema corto inspirado en el Retiro."
      ]
    },
    "Museo Reina Sofía": {
      5: [
        "🔷 Busca un cuadro con formas geométricas y dibuja una igual.",
        "🗿 Imita la pose de un personaje de una escultura.",
        "🎨 Cuenta cuántos colores ves en el Guernica."
      ],
      8: [
        "🖼️ Elige una obra moderna y explica qué te hace sentir.",
        "👨‍🎨 Haz un retrato abstracto de tu familia.",
        "🏷️ Inventa un título divertido para una escultura."
      ],
      12: [
        "📚 Investiga la historia del Guernica y resúmela.",
        "📸 Haz una foto creativa con un reflejo en el museo.",
        "🔍 Crea un reto: ¿puedes encontrar una obra de Dalí?"
      ]
    },
    "Museo Thyssen": {
      5: [
        "🦁 Busca un cuadro con un animal y nómbralo.",
        "😮 Imita la expresión de un retrato.",
        "🔢 Cuenta cuántos cuadros ves en una sala."
      ],
      8: [
        "🎨 Elige tu cuadro favorito y haz un dibujo rápido.",
        "📖 Inventa una historia sobre un personaje de un cuadro.",
        "⛵ Haz una búsqueda: encuentra una obra con un barco."
      ],
      12: [
        "📚 Investiga la historia de una obra impresionista.",
        "📸 Haz una foto artística de un detalle de un cuadro.",
        "� Crea un reto: ¿puedes encontrar una obra de Van Gogh?"
      ]
    }
  };

  // Determinar el rango de edad
  let ageKey;
  if (age < 6) ageKey = 5;
  else if (age <= 9) ageKey = 8;
  else ageKey = 12;

  if (games[location] && games[location][ageKey]) {
    // Selecciona un juego aleatorio de los 3 disponibles
    const options = games[location][ageKey];
    const randomIndex = Math.floor(Math.random() * options.length);
    return options[randomIndex];
  }
  return "No hay juegos disponibles para este lugar.";
}

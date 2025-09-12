import React, { useState, useEffect } from 'react';

const keyframes = {
  fadeIn: {
    '0%': { opacity: 0 },
    '100%': { opacity: 1 }
  },
  jumpAndBounce: {
    '0%, 100%': { transform: 'translateY(0) rotate(0deg)' },
    '25%': { transform: 'translateY(-20px) rotate(-10deg)' },
    '50%': { transform: 'translateY(0) rotate(0deg)' },
    '75%': { transform: 'translateY(-10px) rotate(10deg)' }
  },
  shadowScale: {
    '0%, 100%': {
      transform: 'translateX(-50%) scale(1)',
      opacity: 0.4
    },
    '25%': {
      transform: 'translateX(-50%) scale(0.8)',
      opacity: 0.2
    },
    '50%': {
      transform: 'translateX(-50%) scale(1)',
      opacity: 0.4
    },
    '75%': {
      transform: 'translateX(-50%) scale(0.8)',
      opacity: 0.2
    }
  },
  slideUp: {
    '0%': {
      opacity: 0,
      transform: 'translateY(30px)'
    },
    '100%': {
      opacity: 1,
      transform: 'translateY(0)'
    }
  }
};

const styles = {
  container: (isExiting) => ({
    position: 'fixed',
    top: 0,
    left: 0,
    right: 0,
    bottom: 0,
    background: 'linear-gradient(135deg, #fff5e6 0%, #ffe4cc 100%)',
    display: 'flex',
    justifyContent: 'center',
    alignItems: 'center',
    zIndex: 2000,
    opacity: isExiting ? 0 : 1,
    transition: 'opacity 0.5s ease-out',
    animation: 'fadeIn 0.5s ease-out'
  }),
  mouseCharacter: {
    textAlign: 'center',
    transform: 'translateY(-10%)'
  },
  mouseContainer: {
    position: 'relative',
    display: 'inline-block'
  },
  mouseBody: {
    transformOrigin: 'center',
    animation: 'jumpAndBounce 1.5s ease-in-out infinite'
  },
  mouseEmoji: {
    fontSize: '10rem',
    display: 'inline-block'
  },
  mouseShadow: {
    position: 'absolute',
    bottom: '-10px',
    left: '50%',
    transform: 'translateX(-50%)',
    width: '40px',
    height: '10px',
    background: 'rgba(0, 0, 0, 0.1)',
    borderRadius: '50%',
    animation: 'shadowScale 1.5s ease-in-out infinite'
  },
  welcomeText: {
    marginTop: '2rem',
    opacity: 0,
    animation: 'slideUp 0.5s ease-out 0.7s forwards'
  }
};

// Crear las reglas de animación
const createKeyframeStyle = () => {
  let styleSheet = document.createElement('style');
  styleSheet.id = 'welcome-animation-keyframes';
  
  // Si ya existe, no lo creamos de nuevo
  if (document.getElementById('welcome-animation-keyframes')) return;

  let keyframeRules = Object.entries(keyframes).map(([name, frames]) => {
    const frameRules = Object.entries(frames)
      .map(([key, value]) => `${key} { ${Object.entries(value).map(([prop, val]) => `${prop}: ${val}`).join('; ')} }`)
      .join('\n');
    
    return `@keyframes ${name} {\n${frameRules}\n}`;
  }).join('\n\n');

  styleSheet.textContent = keyframeRules;
  document.head.appendChild(styleSheet);
};

const WelcomeAnimation = ({ onAnimationEnd }) => {
  const [isExiting, setIsExiting] = useState(false);

  useEffect(() => {
    createKeyframeStyle();

    const exitTimer = setTimeout(() => {
      setIsExiting(true);
    }, 4500);

    const endTimer = setTimeout(() => {
      if (onAnimationEnd) {
        onAnimationEnd();
      }
    }, 5000);

    return () => {
      clearTimeout(exitTimer);
      clearTimeout(endTimer);
    };
  }, [onAnimationEnd]);

  return (
    <div style={styles.container(isExiting)}>
      <div style={styles.mouseCharacter}>
        <div style={styles.mouseContainer}>
          <div style={styles.mouseBody}>
            <span role="img" aria-label="ratón" style={styles.mouseEmoji}>
              🐭
            </span>
          </div>
          <div style={styles.mouseShadow}></div>
        </div>
        <div style={styles.welcomeText}>
          <h2 
            className="text-3xl font-bold text-orange-500" 
            style={{ fontFamily: 'Quicksand, sans-serif' }}
          >
            ¡Bienvenidos a Madrid!
          </h2>
          <p 
            className="text-lg text-orange-400 mt-2" 
            style={{ fontFamily: 'Quicksand, sans-serif' }}
          >
            ¡El Ratoncito Pérez os espera!
          </p>
        </div>
      </div>
    </div>
  );
};

export default WelcomeAnimation;

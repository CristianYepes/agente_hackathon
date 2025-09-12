// frontend/src/components/ChatView.js
import React, { useState, useEffect, useRef } from 'react';
import ApiService from '../services/api';

const ChatView = () => {
  const [messages, setMessages] = useState([]);
  const [inputMessage, setInputMessage] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [isConnected, setIsConnected] = useState(true); // Cambiar a true por defecto
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  useEffect(() => {
    // Mensaje de bienvenida
    addBotMessage("¡Hola! Soy el Ratoncito Pérez 🐭✨ ¡Bienvenidos a Madrid! ¿Estás listo para explorar la ciudad conmigo?");

    // Verificar conexión después de un pequeño delay
    setTimeout(() => {
      checkConnection();
    }, 1000);
  }, []);

  const checkConnection = async () => {
    try {
      const response = await ApiService.healthCheck();
      console.log('✅ Backend conectado:', response);
      setIsConnected(true);
    } catch (error) {
      console.error('❌ Error conectando con el backend:', error);
      setIsConnected(false);
    }
  };

  const addMessage = (text, sent = false, isError = false) => {
    const newMessage = {
      text,
      sent,
      isError,
      timestamp: Date.now()
    };
    setMessages(prev => [...prev, newMessage]);
  };

  const addBotMessage = (text) => addMessage(text, false);

  const handleSendMessage = async () => {
    if (!inputMessage.trim() || isLoading) return; // Remover !isConnected

    const userMessage = inputMessage.trim();
    setInputMessage('');
    setIsLoading(true);

    // Agregar mensaje del usuario inmediatamente
    addMessage(userMessage, true);

    try {
      console.log('📤 Enviando mensaje:', userMessage);

      // Enviar al backend
      const response = await ApiService.sendMessage(userMessage);

      console.log('📥 Respuesta recibida:', response);

      // Agregar respuesta del Ratoncito Pérez
      addBotMessage(response.message || "¡Hola! Soy el Ratoncito Pérez 🐭✨");

    } catch (error) {
      console.error('❌ Error enviando mensaje:', error);
      addMessage("¡Oops! Parece que tengo problemas técnicos. ¿Puedes intentar de nuevo? 🐭💫", false, true);
    } finally {
      setIsLoading(false);
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSendMessage();
    }
  };

  return (
    <div className="flex flex-col h-screen bg-gradient-to-b from-blue-50 to-orange-50">
      {/* Status de conexión */}
      <div className={`p-3 text-center text-sm font-medium transition-all duration-300 ${
        isConnected
          ? 'bg-green-100 text-green-800 border-b border-green-200'
          : 'bg-red-100 text-red-800 border-b border-red-200'
      }`}>
        {isConnected ? '🟢 Conectado con el Ratoncito Pérez' : '🔴 Reconectando...'}
        <button
          onClick={checkConnection}
          className="ml-2 text-xs underline hover:no-underline transition-all duration-200"
        >
          {isConnected ? 'Probar conexión' : 'Reintentar'}
        </button>
      </div>

      {/* Mensajes */}
      <div className="flex-1 overflow-y-auto p-4 space-y-4">
        {messages.map((message, index) => (
          <div
            key={index}
            className={`flex ${message.sent ? 'justify-end' : 'justify-start'} transition-all duration-300`}
          >
            <div className={`max-w-xs lg:max-w-md px-4 py-3 rounded-2xl shadow-sm transition-all duration-200 hover:shadow-md ${
              message.sent
                ? 'bg-orange-500 text-white rounded-br-md'
                : message.isError
                  ? 'bg-red-100 text-red-800 border border-red-300 rounded-bl-md'
                  : 'bg-white text-gray-800 border border-gray-200 rounded-bl-md'
            }`}>
              <p className="text-sm leading-relaxed whitespace-pre-wrap">{message.text}</p>
              <span className="text-xs opacity-70 mt-2 block">
                {new Date(message.timestamp).toLocaleTimeString()}
              </span>
            </div>
          </div>
        ))}

        {/* Indicador de escritura */}
        {isLoading && (
          <div className="flex justify-start animate-pulse">
            <div className="bg-gray-200 px-4 py-3 rounded-2xl rounded-bl-md">
              <div className="flex space-x-1">
                <div className="w-2 h-2 bg-gray-500 rounded-full animate-bounce"></div>
                <div className="w-2 h-2 bg-gray-500 rounded-full animate-bounce" style={{animationDelay: '0.1s'}}></div>
                <div className="w-2 h-2 bg-gray-500 rounded-full animate-bounce" style={{animationDelay: '0.2s'}}></div>
              </div>
            </div>
          </div>
        )}

        <div ref={messagesEndRef} />
      </div>

      {/* Input de mensaje */}
      <div className="border-t bg-white p-4 shadow-lg">
        <div className="flex space-x-3 max-w-4xl mx-auto">
          <input
            type="text"
            value={inputMessage}
            onChange={(e) => setInputMessage(e.target.value)}
            onKeyPress={handleKeyPress}
            placeholder="Escribe tu mensaje al Ratoncito Pérez..."
            disabled={isLoading} // Solo deshabilitar cuando está cargando
            className="flex-1 border border-gray-300 rounded-full px-6 py-3
              focus:outline-none focus:ring-2 focus:ring-orange-500 focus:border-transparent
              disabled:bg-gray-100 disabled:cursor-not-allowed
              transition-all duration-200 placeholder-gray-400"
          />
          <button
            onClick={handleSendMessage}
            disabled={isLoading || !inputMessage.trim()} // Solo deshabilitar cuando está cargando o no hay texto
            className="bg-orange-500 text-white px-8 py-3 rounded-full
              hover:bg-orange-600 focus:outline-none focus:ring-2 focus:ring-orange-500
              disabled:bg-gray-300 disabled:cursor-not-allowed
              transition-all duration-200 font-medium transform hover:scale-105 active:scale-95"
          >
            {isLoading ? '⏳' : '📤 Enviar'}
          </button>
        </div>
      </div>
    </div>
  );
};

export default ChatView;

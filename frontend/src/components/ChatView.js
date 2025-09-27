import React, { useState, useEffect } from 'react';

const ChatView = () => {
		const [messages, setMessages] = useState([]);
		const [isFirstVisit, setIsFirstVisit] = useState(true);
		const [inputMessage, setInputMessage] = useState('');

		const keyframesCSS = `
				@keyframes fadeIn {
						from {
								opacity: 0;
								transform: translateY(10px);
						}
						to {
								opacity: 1;
								transform: translateY(0);
						}
				}
		`;

		useEffect(() => {
				if (isFirstVisit && messages.length === 0) {
						const welcomeMessage = {
								text: "¡Hola! Soy el Ratoncito Pérez 🐭 ¡Bienvenidos a Madrid! Pregúntame cualquier cosa sobre nuestra aventura por la ciudad, los lugares que hemos visto en el mapa, o cuéntame si habéis perdido algún diente recientemente... 🦷✨",
								sent: false,
								isWelcome: true,
								timestamp: Date.now()
						};

						setTimeout(() => {
								setMessages([welcomeMessage]);
						}, 500);
				}
		}, [isFirstVisit, messages.length]);

		const handleSendMessage = (e) => {
				e.preventDefault();
				if (inputMessage.trim()) {
						setMessages(prevMessages => {
								const filteredMessages = prevMessages.filter(msg => !msg.isWelcome);
								return [...filteredMessages, { text: inputMessage, sent: true, timestamp: Date.now() }];
						});
						setInputMessage('');
						setIsFirstVisit(false);
				}
		};

		return (
				<>
						<style>{keyframesCSS}</style>
						<div className="flex flex-col h-[calc(100vh-10rem)] md:h-[calc(100vh-4rem)] mt-16 md:mt-20 bg-white">
								<div className="flex-grow overflow-y-auto px-4 py-5 pb-32 md:pb-20">
										{messages.length === 0 && !isFirstVisit && (
												<div className="flex items-center justify-center h-full text-gray-400">
														<p style={{ fontFamily: 'Quicksand, sans-serif' }}>
																Comienza una conversación con el Ratoncito Pérez...
														</p>
												</div>
										)}

										{messages.map((message, index) => (
												<div
														key={index}
														className={`my-3 p-3 rounded-xl max-w-[80%] shadow-sm transition-all duration-300 ${
																message.sent
																		? 'bg-gradient-to-r from-orange-400 to-orange-500 text-white ml-auto'
																		: 'bg-gradient-to-r from-blue-50 to-purple-50 border-2 border-orange-200 text-gray-700 mr-auto'
														}`}
														style={{
																fontFamily: 'Quicksand, sans-serif',
																animation: message.isWelcome ? 'fadeIn 0.6s ease-out' : 'none'
														}}
												>
														{!message.sent && (
																<div className="flex items-center gap-2 mb-1">
																		<span className="text-lg">🐭</span>
																		<span className="text-xs font-semibold text-orange-500">Ratoncito Pérez</span>
																</div>
														)}
														{message.text}
												</div>
										))}
								</div>

								<form
										className="fixed bottom-[5rem] md:bottom-4 left-0 right-0 flex p-4 pb-8 md:pb-4 border-t border-orange-200 bg-white shadow-lg"
										onSubmit={handleSendMessage}
										style={{ fontFamily: 'Quicksand, sans-serif' }}
								>
										<input
												type="text"
												value={inputMessage}
												onChange={(e) => setInputMessage(e.target.value)}
												placeholder={isFirstVisit ? "Escribe tu primer mensaje al Ratoncito Pérez..." : "Escribe un mensaje..."}
												className="flex-grow p-3 mr-3 border-2 border-orange-200 rounded-xl focus:border-orange-400 focus:ring-2 focus:ring-orange-200 focus:outline-none transition-colors"
												style={{ fontFamily: 'Quicksand, sans-serif' }}
										/>
										<button
												type="submit"
												className="px-6 py-3 bg-gradient-to-r from-orange-400 to-orange-500 text-white font-semibold rounded-xl cursor-pointer hover:from-orange-500 hover:to-orange-600 transition-all transform hover:scale-105 shadow-lg"
												style={{ fontFamily: 'Quicksand, sans-serif' }}
										>
												Enviar
										</button>
								</form>
						</div>
				</>
		);
};

export default ChatView;
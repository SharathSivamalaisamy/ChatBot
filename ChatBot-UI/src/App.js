import React, { useState } from 'react';
import './App.css';

function App() {
  const [userInput, setUserInput] = useState('');
  const [responses, setResponses] = useState([]);

  const handleInputChange = (e) => {
    setUserInput(e.target.value);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!userInput.trim()) return;

    // Here you would send the userInput to your backend for processing
    // For now, let's just mock a response
    const mockResponse = `Mock response to: ${userInput}`;

    setResponses([...responses, { question: userInput, answer: mockResponse }]);
    setUserInput(''); // Reset input field
  };

  return (
    <div className="App">
      <h1>Chatbot UI</h1>
      <form onSubmit={handleSubmit}>
        <input
          type="text"
          value={userInput}
          onChange={handleInputChange}
          placeholder="Ask me anything..."
        />
        <button type="submit">Send</button>
      </form>
      <div className="responses">
        {responses.map((resp, index) => (
          <div key={index} className="response">
            <strong>Q:</strong> {resp.question}
            <br />
            <strong>A:</strong> {resp.answer}
          </div>
        ))}
      </div>
    </div>
  );
}

export default App;

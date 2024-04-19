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
  
    // Send the userInput to the backend using the fetch API
    try {
      // const response = await fetch(`${process.env.REACT_APP_API_URL}/chat`, {
        const response = await fetch('http://10.93.142.95:8080/chat', {  
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ user_input: userInput }),
      });
  
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
  
      const data = await response.json();
      setResponses([...responses, { question: userInput, answer: data.answer }]);
    } catch (error) {
      console.error("Could not get a response: ", error);
    }
  
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

import './App.css';
import React, { useState } from 'react';

function App() {
  const [userData, setUserData] = useState([]);
  const [productData, setProductData] = useState([]);
  const [userInput, setUserInput] = useState('');
  const [productInput, setProductInput] = useState('');

  const fetchUserData = () => {
    fetch(`http://127.0.0.1:8000/api/recommendations/${userInput}`, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
      },
    })
      .then(response => response.json())
      .then(data => setUserData(data.recommendations))
      .catch(error => console.error('Error fetching user data:', error));
  };

  const fetchProductData = () => {
    fetch(`http://127.0.0.1:8000/api/users/${productInput}`, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
      },
    })
      .then(response => response.json())
      .then(data => setProductData(data.users))
      .catch(error => console.error('Error fetching product data:', error));
  };

  const handleUserInputChange = event => {
    setUserInput(event.target.value);
  };

  const handleProductInputChange = event => {
    setProductInput(event.target.value);
  };

  const handleUserSubmit = event => {
    event.preventDefault();
    fetchUserData();
  };

  const handleProductSubmit = event => {
    event.preventDefault();
    fetchProductData();
  };

  return (
    <div>
      <section className="recommendation-section">
        <h2>User Recommendations</h2>
        <form onSubmit={handleUserSubmit}>
          <label>
            Enter User:
            <input type="text" value={userInput} onChange={handleUserInputChange} />
          </label>
          <button type="submit">Get User Recommendations</button>
        </form>
  
        {userData.map(item => (
          <div key={item}>{item}</div>
        ))}
      </section>
  
      <section className="recommendation-section">
        <h2>Product Recommendations</h2>
        <form onSubmit={handleProductSubmit}>
          <label>
            Enter Product:
            <input type="text" value={productInput} onChange={handleProductInputChange} />
          </label>
          <button type="submit">Get Product Recommendations</button>
        </form>
  
        {productData.map(item => (
          <div key={item}>{item}</div>
        ))}
      </section>
    </div>
  );
}

export default App;


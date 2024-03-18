import { useCallback, useEffect, useState } from 'react';
import logo from './logo.svg';
import './App.css';

const App = () => {
  const [time, setTime] = useState('');

  const fetchAPI = useCallback(async () => {
    const res = await fetch('/api');
    const { data } = await res.json();
    setTime(data);
  }, []);

  useEffect(() => {
    fetchAPI();
  }, [fetchAPI]);

  return (
    <div className="App">
      <header className="App-header">
        <img src={logo} className="App-logo" alt="logo" />
        <p>
          Edit <code>src/App.js</code> and save to reload.
        </p>
        <a
          className="App-link"
          href="https://reactjs.org"
          target="_blank"
          rel="noopener noreferrer"
        >
          Learn React
        </a>
        <p>{time}</p>
      </header>
    </div>
  );
}

export default App;

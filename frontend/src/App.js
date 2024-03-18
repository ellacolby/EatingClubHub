import { useCallback, useEffect } from 'react';
import logo from './logo.svg';
import './App.css';

function App() {

  const fetchAPI = useCallback(async () => {
    const res = await fetch('/api');
    const { data } = await res.json();
    console.log(data);
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
      </header>
    </div>
  );
}

export default App;

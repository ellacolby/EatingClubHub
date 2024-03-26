import { useCallback, useEffect, useState } from "react";

// internal imports
import logo from "../logo.svg";
import "../App.css";

// utils
import get from "../utils/get";

const Home = () => {
  const [data, setData] = useState("");

  const logout = async () => {
    const res = await fetch("/logout");
    const data = await res.json();
    window.location.href = data["logout_url"];
  };

  const fetchClubs = async () => {
    const data = await get("/clubs");
    if (data) {
      setData(data.data);
    }
  };

  const fetchAPI = useCallback(async () => {
    // logout();
    fetchClubs();
  }, []);

  useEffect(() => {
    // fetchAPI();
  }, [fetchAPI]);

  return (
    <div className="App">
      <header className="App-header">
        <img src={logo} className="App-logo" alt="logo" />
        <p>
          Edit <code>HELLO WORLD</code> and save to reload.
        </p>
        <a
          className="App-link"
          href="https://reactjs.org"
          target="_blank"
          rel="noopener noreferrer"
        >
          Learn React
        </a>
        <p>{data}</p>
        <button onClick={() => logout()}>Log Out</button>
        <button onClick={() => fetchClubs()}>Log In</button>
        <a href="/contact">Contact Officers</a>
      </header>
    </div>
  );
};

export default Home;

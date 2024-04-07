import { useCallback, useEffect, useState } from "react";

import "../App.css";

// utils
import get from "../utils/get";

const HomePage = () => {
  const [data, setData] = useState("");
  const [clubs, setClubs] = useState([]);

  const fetchClubs = async () => {
    const data = await get("/api/clubs");
    console.log(data);
    if (data) {
      setClubs(data);
    }
  };

  return (
    <div className="App">
      <header className="App-header">
        <p>{data}</p>
        {clubs.map((club) => (
          <button
            onClick={() => {
              setData(club[2]);
            }}
          >
            {club[1]}
          </button>
        ))}
        <button onClick={() => fetchClubs()}>Fetch Clubs</button>
        <a href="/logout">Log Out</a>
        <a href="/contact">Contact Officers</a>
        <a href="/events">See Event Calendar</a>
      </header>
    </div>
  );
};

export default HomePage;

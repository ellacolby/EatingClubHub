import { useCallback, useEffect, useState } from "react";

// utils
import get from "../utils/get";

const HomePage = () => {
  const [data, setData] = useState("");
  const [clubs, setClubs] = useState([]);

  const logout = async () => {
    const res = await get("/logout");
    window.location.href = res["logout_url"];
  };

  const fetchClubs = async () => {
    const data = await get("/clubs");
    console.log(data);
    if (data) {
      // setData(data);
      setClubs(data);
    }
  };

  const fetchAPI = useCallback(async () => {
    fetchClubs();
  }, []);

  useEffect(() => {
    // fetchAPI();
  }, [fetchAPI]);

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
        <button onClick={() => logout()}>Log Out</button>
        <button onClick={() => fetchClubs()}>Fetch Clubs</button>
        <a href="/contact">Contact Officers</a>
      </header>
    </div>
  );
};

export default HomePage;

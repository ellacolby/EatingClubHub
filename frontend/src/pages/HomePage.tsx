import { useCallback, useEffect, useState } from "react";

// utils
import get from "../utils/get";

const HomePage = () => {
  const [data, setData] = useState('');

  const logout = async () => {
    const res = await get('/logout');
    window.location.href = res['logout_url'];
  };

  const fetchClubs = async () => {
    const data = await get('/clubs');
    if (data) {
      setData(data);
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
        <button onClick={() => logout()}>Log Out</button>
        <button onClick={() => fetchClubs()}>Fetch Clubs</button>
        <a href="/contact">Contact Officers</a>
      </header>
    </div>
  );
};

export default HomePage;

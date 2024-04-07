import { useCallback, useEffect, useState } from "react";
// internal imports
import HomePage from "./pages/HomePage";
import LoginPage from "./pages/LoginPage";
import ContactClub from "./pages/ContactClubPage";
import CalendarPage from "./pages/CalendarPage";

// external imports
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";

// utils
import get from "./utils/get";

type TokenResponse = { username: string } | { login_url: string } | null;

const App = () => {
  const [token, setToken] = useState<TokenResponse>(null);

  const getUsername = useCallback(async () => {
    // const res: TokenResponse = await get("/api/login");
    // if (res && 'login_url' in res) {
    //   // if (window.location.pathname !== '/') {
    //   //   window.location.href = '/';
    //   // }
    // }
    // setToken(res);
  }, []);

  useEffect(() => {
    getUsername();
  }, [getUsername]);

  return (
    <Router>
      <Routes>
        {
          <>
            <Route path="/" element={<HomePage />} />
            <Route path="/contact" element={<ContactClub />} />
            <Route path="/events" element={<CalendarPage />} />
          </>
        }
      </Routes>
    </Router>
  );
};

export default App;

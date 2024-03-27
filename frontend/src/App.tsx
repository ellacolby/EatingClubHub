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

const App = () => {
  const [loginUrl, setLoginUrl] = useState<string | null>(null);

  const getUsername = useCallback(async () => {
    const data = await get("/login");
    if (data["login_url"]) {
      if (window.location.pathname !== "/") {
        window.location.href = "/";
      }
      setLoginUrl(data["login_url"]);
    } else {
      setLoginUrl(null);
    }
  }, []);

  useEffect(() => {
    getUsername();
  }, [getUsername]);

  return (
    <Router>
      <Routes>
        <Route
          path="/"
          element={loginUrl ? <LoginPage loginUrl={loginUrl} /> : <HomePage />}
        ></Route>
        {!loginUrl && (
          <>
            <Route path="/contact" element={<ContactClub />}></Route>
            <Route path="/events" element={<CalendarPage />}></Route>
          </>
        )}
      </Routes>
    </Router>
  );
};

export default App;

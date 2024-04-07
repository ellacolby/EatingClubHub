// pages
import HomePage from "./pages/HomePage";
import ContactClub from "./pages/ContactClubPage";
import CalendarPage from "./pages/CalendarPage";

// external imports
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";

const App = () => {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<HomePage />} />
        <Route path="/contact" element={<ContactClub />} />
        <Route path="/events" element={<CalendarPage />} />
      </Routes>
    </Router>
  );
};

export default App;

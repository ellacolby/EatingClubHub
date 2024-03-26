// internal imports
import Home from "./pages/Home";
import ContactClub from "./pages/ContactClubPage";

// external imports
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";


const App = () => {
  return (
    <Router>
      <Routes>
        <Route path="/contact" element={<ContactClub />}></Route>
        <Route path="/" element={<Home />}></Route>
      </Routes>
    </Router>
  );
};

export default App;

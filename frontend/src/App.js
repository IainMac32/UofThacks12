import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import HomePage from "./homepage.js";
import AboutPage from "./option.js";
import Slideshow from "./slideshow.js";

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<HomePage />} />
        <Route path="/about" element={<AboutPage />} />
        <Route path="/slideshow" element={<Slideshow />} />
      </Routes>
    </Router>
  );
}

export default App;
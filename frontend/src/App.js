import React from "react";
// import { BrowserRouter as Router, Routes, Route, Link } from "react-router-dom";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import HomePage from "./HomePage";
import LearningMaterial from "./LearningMaterial";
import EssayPolish from "./EssayPolish";
import PracticeList from "./PracticeList";
import PracticeTest from "./PracticeTest";
import PracticeResult from "./PracticeResult";
import PracticeSample from "./PracticeSample";

export default function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<HomePage />} />
        <Route path="/polish" element={<EssayPolish />} />
        <Route path="/material" element={<LearningMaterial />} />
        <Route path="/practice" element={<PracticeList />} />
        <Route path="/practice/:bookId/:testId" element={<PracticeTest />} />
        <Route path="/practice/:bookId/:testId/result" element={<PracticeResult />} />
        <Route path="/practice/:bookId/:testId/sample" element={<PracticeSample />} />
      </Routes>
    </Router>
  );
}

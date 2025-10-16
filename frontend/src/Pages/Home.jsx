import React from "react";
import { useNavigate } from "react-router-dom";
import Header from "../components/Header";

export default function Home() {
  const navigate = useNavigate();

  const handleGetStarted = () => {
    navigate("/signin");
  };

  return (
    <div className="home-container">
      <Header></Header>
      <div className="hero-section">
        <h1>Welcome to JobLexa Analytics</h1>
        <h2>Your resume, analyzed by AI for a competitive advantage</h2>
        <p>
          We identify critical market skills and provide you with a precise
          matching score to optimize your application.
        </p>
        <br></br>
        <button className="cta-button" onClick={handleGetStarted}>
          Get Started
        </button>
      </div>

      <section className="functioning">
        <h2>It's simple and effective in 3 steps</h2>
        <div className="steps">
          <div className="step-card">
            <h3>1. Search for the job</h3>
            <p>
              Enter the job title and the geographic area (city, province) to
              receive the 35 most requested skills.
            </p>
          </div>
          <div className="step-card">
            <h3>2. Upload your CV</h3>
            <p>Upload your CV in PDF or DOCX format.</p>
          </div>
          <div className="step-card">
            <h3>3. Get your score</h3>
            <p>
              Receive your score in % along with the precise steps to optimize
              your profile.
            </p>
          </div>
        </div>
      </section>

      <footer>© 2025 JobLexa Analytics. All rights reserved.</footer>
    </div>
  );
}

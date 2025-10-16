import React from "react";
import Header from "../components/Header";

export default function About() {
  return (
    <div className="about-container">
      <Header />

      <div className="hero-section">
        <h1>JobLexa Analytics:</h1>
        <h2>Turning uncertainty into a career strategy</h2>
        <p>
          We created JobLexa Analytics to eliminate guesswork from the job
          search process. Our mission is to provide professionals with clear,
          actionable, and AI-validated data on what the job market really
          demands. No more generic CVs — we offer you a precise roadmap for
          landing the job you are aiming for.
        </p>
      </div>

      <section className="functioning">
        <h2>JobLexa Analytics’ 3-Step Methodology</h2>
        <div className="steps">
          <div className="step-card">
            <h3>1. Real-Time Market Analysis</h3>
            <p>
              We identify the correct labour-market requirements for the
              targeted job and region. By analyzing the latest job offers, the
              system provides you with the top 30 skills that companies are
              actively looking for.
            </p>
          </div>

          <div className="step-card">
            <h3>2. CV Correspondence Score by AI</h3>
            <p>
              Provide your CV and receive an accurate percentage match (0–100%)
              based on market requirements (Step 1). AI evaluates your CV not
              only on the presence of keywords but also on the contextual
              evidence of your experience.
            </p>
          </div>

          <div className="step-card">
            <h3>3. Personalized Action Plan</h3>
            <p>
              The application turns the diagnosis into a solution. It gives you
              a clear roadmap, highlighting critical missing skills and
              providing concrete suggestions on how to reformulate your CV to
              maximize your score.
            </p>
          </div>
        </div>
      </section>

      <footer>© 2025 JobLexa Analytics. All rights reserved.</footer>
    </div>
  );
}

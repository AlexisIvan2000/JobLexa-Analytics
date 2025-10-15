import React, { useState, useRef,useEffect } from "react";
import { auth, jobService } from "../services/api";
import Logo from "../assets/logo-square.svg";
import { useNavigate } from "react-router-dom";

export default function Dashboard() {

  const navigate = useNavigate();

  useEffect(() =>{
    const token = localStorage.getItem("access_token");
    if (!token){
      navigate("/signin");
    }
  }, [navigate])
  const [jobTitle, setJobTitle] = useState("");
  const [city, setCity] = useState("");
  const [state, setState] = useState("");
  const [skills, setSkills] = useState(null);
  const [file, setFile] = useState(null);
  const [loadingSkills, setLoadingSkills] = useState(false);
  const [loadingAnalysis, setLoadingAnalysis] = useState(false);
  const [error, setError] = useState("");
  const [matchResult, setMatchResult] = useState(null);

  const fileInputRef = useRef(null);

  const handleSearchSkills = async () => {
    setLoadingSkills(true);
    setError("");
    setSkills(null);

    if (!jobTitle || !city || !state) {
      setError("Please fill all fields before searching.");
      setLoadingSkills(false);
      return;
    }

    try {
      const response = await jobService.searchSkills(jobTitle, city, state);
      console.log("API Response:", response.data);

      if (response.data.success) {
        setSkills(response.data.skills || {});
      } else {
        setError(response.data.message || "No skills found.");
      }
    } catch (err) {
      console.error("Error fetching skills:", err);
      setError("Unable to fetch skills. Please try again later.");
    } finally {
      setLoadingSkills(false);
    }
  };

  const handleAnalyzeResume = async () => {
    if (!file) {
      setError("Please upload your CV first.");
      return;
    }
    setLoadingAnalysis(true);
    setError("");
    setMatchResult(null);

    try {
      const response = await jobService.getScore(file);
      setMatchResult(response.data);
    } catch (err) {
      console.error("Error analyzing resume:", err);
      setError(err.response?.data?.message || "Error analyzing resume.");
    } finally {
      setLoadingAnalysis(false);
    }
  };

  const handleReset = () => {
    setJobTitle("");
    setCity("");
    setState("");
    setSkills(null);
    setFile(null);
    setMatchResult(null);
    setError("");

    if (fileInputRef.current) {
      fileInputRef.current.value = "";
    }
  };

  const handleLogout = () => {
    auth.signout();
    window.location.href = "/";
  };

  return (
    <div className="dashboard-container">
      <div className="header-section">
        <header>
          <div className="logo-title">
            <img src={Logo} alt="JobLexa Logo" className="logo-img" />
            <h1>JobLexa Analytics</h1>
          </div>
          <div className="header-button">
            <button className="cta-button" onClick={handleLogout}>
              Logout
            </button>
            <button className="cta-button" onClick={handleReset}>
              Reset
            </button>
          </div>
        </header>
      </div>

      <div className="main-section">
        <h3>Welcome to your Dashboard</h3>
        <p>
          The era of guessing is over. Get your AI Match Score now to turn
          market demands into your next interview.
        </p>
      </div>

      <div className="horizontal-sections">
        <div className="section-card">
          <h3> Search Job Skills</h3>
          <label>Job Title</label>
          <input
            type="text"
            value={jobTitle}
            placeholder="e.g., Data Scientist"
            onChange={(e) => setJobTitle(e.target.value)}
          />
          <label>City</label>
          <input
            type="text"
            value={city}
            placeholder="e.g., Montreal"
            onChange={(e) => setCity(e.target.value)}
          />
          <label>State / Province</label>
          <input
            type="text"
            value={state}
            placeholder="e.g., QC"
            onChange={(e) => setState(e.target.value)}
          />
          <button className="cta-button" onClick={handleSearchSkills}>
            {loadingSkills ? "Searching..." : "Search Skills"}
          </button>
          {error && <p className="error-message">{error}</p>}
          {skills && (
            <div className="results-section">
              <h4>Recommended Skills</h4>
              {Object.entries(skills).map(([category, list]) => (
                <div className="skill-category" key={category}>
                  <h5>{category.replace(/_/g, " ")}</h5>
                  <ul>
                    {list.map((skill, idx) => (
                      <li key={idx}>{skill}</li>
                    ))}
                  </ul>
                </div>
              ))}
            </div>
          )}
        </div>
        <div className="section-card">
          <h3> Analyze Your Resume</h3>
          <p>Upload your resume (PDF or DOCX) to get your AI Match Score</p>
          <input
            ref={fileInputRef}
            type="file"
            accept=".pdf,.docx"
            onChange={(e) => setFile(e.target.files[0])}
          />
          <button className="cta-button" onClick={handleAnalyzeResume}>
            {loadingAnalysis ? "Analyzing..." : "Analyze Resume"}
          </button>
          {matchResult && (
            <div className="match-result">
              <h4>Analysis Result</h4>
              <p>
                Match Score: <strong>{matchResult.match_score}%</strong>
              </p>
              <p>
                Missing Skills:{" "}
                {matchResult.missing_skills?.length
                  ? matchResult.missing_skills.join(", ")
                  : "None"}
              </p>
              <p>Suggestion: {matchResult.suggestion}</p>
            </div>
          )}
        </div>
      </div>
      <footer>© 2025 JobLexa Analytics. All rights reserved.</footer>
    </div>
  );
}

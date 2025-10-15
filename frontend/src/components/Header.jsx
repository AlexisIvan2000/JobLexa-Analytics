import React from "react";
import { useNavigate } from "react-router-dom";
import Logo from "../assets/logo-square.svg";

export default function Header() {
  const navigate = useNavigate();
  const GoHome = () => {
    navigate("/");
  };
  const About = () => {
    navigate("/about");
  };

  return (
    <div className="header-section">
      <header>
        <div className="logo-title">
          <img src={Logo} alt="JobLexa Logo" className="logo-img" />
          <h1>JobLexa Analytics</h1>
        </div>
        <div className="header-button">
          <button className="cta-button" onClick={GoHome}>
            Home
          </button>

          <button className="cta-button" onClick={About}>
            About
          </button>
        </div>
      </header>
    </div>
  );
}

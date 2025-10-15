import React, { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { auth } from "../services/api";

export default function Signup() {
  const navigate = useNavigate();
  const [firstName, setFirstName] = useState("");
  const [lastName, setLastName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");

    try {
      const userData = { 
        first_name: firstName,
        last_name: lastName,
        email: email,
        password: password
      };
      await auth.signup(userData);
      alert("Registration successful! Please log in.");
      navigate("/signin");
    } catch (err) {
      const message =
        err.response?.data?.detail || "Registration failed. Please try again.";
      setError(message);
      alert(message);
      //console.error("Registration error:", err);
    }
  };

  const handleGoogleLogin = () => {
    auth.googleLogin();
  };

  return (
    <div className="signup-container">
      <h1>Register</h1>
      <form className="register-form">
        <h2>Account information</h2>
        <p>Fill all form field to go to next step</p>
        <div className="for-firstname">
          <label htmlFor="firstName">Enter your first name</label>
          <input
            type="text"
            id="firstName"
            value={firstName}
            onChange={(e) => setFirstName(e.target.value)}
            placeholder="first name"
          ></input>
        </div>
        <div className="for-lastname">
          <label htmlFor="lastName">Enter your last name</label>
          <input
            type="text"
            id="lastName"
            value={lastName}
            onChange={(e) => setLastName(e.target.value)}
            placeholder="last name"
          ></input>
        </div>

        <div className="for-email">
          <label htmlFor="email">Enter your email</label>
          <input
            type="email"
            id="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            placeholder="email"
          ></input>
        </div>
        <div className="for-password">
          <label htmlFor="password">Enter your password</label>
          <input
            type="password"
            id="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            placeholder="password"
          ></input>
        </div>
        <div>
          <button className="cta-button" onClick={handleSubmit} type="submit">
            Register
          </button>
          <button className="cta-button" onClick={handleGoogleLogin}>
            Continue with Google
          </button>
        </div>

        <div>
          <p>
            Already have an account? <Link to="/signin">Sign in</Link>
          </p>
        </div>
      </form>
      {error && <p className="error-message">{error}</p>}
    </div>
  );
}

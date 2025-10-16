import React, { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { auth } from "../services/api";

export default function Signin() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");

    try {
      const response = await auth.signin({ email, password });

      localStorage.setItem("access_token", response.data.token);

      alert("Login successful!");
      navigate("/dashboard");
    } catch (err) {
      const message =
        err.response?.data?.detail ||
        "Login failed. Please try again (wrong email or password)";
      setError(message);
      alert(message);
      //console.error("Login error:", err);
    }
  };

  const handleGoogleLogin = () => {
    auth.googleLogin();
  };

  return (
    <div className="signin-container">
      <h1>Login</h1>
      <form className="login-form">
        <h2>Welcome back! Please login to your account</h2>
        <div className="for-email">
          <label htmlFor="email">Enter your email </label>
          <br></br>
          <input
            type="email"
            id="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            placeholder="Email"
            required
          ></input>
        </div>
        <div className="for-password">
          <label htmlFor="password">Enter your password</label>
          <br></br>
          <input
            type="password"
            id="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            placeholder="******"
            required
          ></input>
        </div>
        <div>
          <button className="cta-button" onClick={handleSubmit} type="submit">
            Login
          </button>

          <button
            className="cta-button"
            onClick={handleGoogleLogin}
            type="button"
          >
            Continue with Google
          </button>
        </div>
        <p>
          Don't have an account? <Link to="/signup">Sign up</Link>
        </p>
      </form>
      {error && <p className="error-message">{error}</p>}
    </div>
  );
}

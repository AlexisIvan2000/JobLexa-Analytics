import Home from "../pages/Home";
import About from "../pages/About";
import Signin from "../pages/Signin";
import Signup from "../pages/Signup";
import Dashboard from "../pages/Dashboard";
import OAuthCallback from "./components/OAuthCallback";
import React from "react";
import {
  BrowserRouter as Router,
  Routes,
  Route,
 
  BrowserRouter,
} from "react-router-dom";
import "./App.css";

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Home></Home>}></Route>
        <Route path="/about" element={<About></About>}></Route>
        <Route path="/signin" element={<Signin></Signin>}></Route>
        <Route path="/signup" element={<Signup></Signup>}></Route>
        <Route path="/dashboard" element={<Dashboard></Dashboard>}></Route>
        <Route path="/oauth/callback" element={<OAuthCallback></OAuthCallback>} ></Route>

      </Routes>
    </BrowserRouter>
  );
}

export default App;

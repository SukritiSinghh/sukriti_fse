// This file has been renamed to Navbar.jsx
import React from 'react';
import { Link } from 'react-router-dom';
import './Navbar.css';

const Navbar = () => {
  return (
    <nav className="navbar">
      <div className="navbar-logo">
        <Link to="/">InsureTech</Link>
      </div>
      {/* <div className="navbar-links">
        <Link to="/">Home</Link>
        <Link to="/features">Features</Link>
        <Link to="/about">About</Link>
        <Link to="/contact">Contact</Link>
      </div> */}
      <div className="navbar-auth">
        <Link to="/login" className="login-btn">Login</Link>
        <Link to="/signup" className="signup-btn">Sign Up</Link>
      </div>
    </nav>
  );
};

export default Navbar;

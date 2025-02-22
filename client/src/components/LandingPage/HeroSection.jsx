// This file has been renamed to HeroSection.jsx
import React from 'react';
import { Link } from 'react-router-dom';
import './HeroSection.css';

const HeroSection = () => {
  return (
    <section className="hero-section">
      <div className="hero-content">
        <h1>AI-Powered Finance & Insurance Management for Your Organization</h1>
        <p>Seamlessly process financial data, automate claims, and gain AI-driven insights.</p>
        <Link to="/signup" className="cta-button">
          Get Started – Create Your Organization
        </Link>
      </div>
      <div className="hero-illustration">
        {/* Add your illustration or animation here */}
        <div className="animation-placeholder">
          {/* This will be replaced with actual animation */}
        </div>
      </div>
    </section>
  );
};

export default HeroSection;

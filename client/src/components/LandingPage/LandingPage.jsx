// This file has been renamed to LandingPage.jsx
import React from 'react';
import Navbar from './Navbar';
import HeroSection from './HeroSection';
import Features from './Features';
import HowItWorks from './HowItWorks';
import Footer from './Footer';
import './LandingPage.css';

const LandingPage = () => {
  return (
    <div className="landing-page">
      <Navbar />
      <main>
        <HeroSection />
        <Features />
        <HowItWorks />
        <section className="cta-section">
          <h2>Ready to Simplify Finance & Insurance?</h2>
          <p>Get Started Today!</p>
          <div className="cta-buttons">
            <button className="cta-button primary">Sign Up</button>
            <button className="cta-button secondary">Request a Demo</button>
          </div>
        </section>
      </main>
      <Footer />
    </div>
  );
};

export default LandingPage;

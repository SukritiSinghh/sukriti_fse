// This file has been renamed to HomePage.jsx
import React from 'react';
import Navbar from './Navbar.jsx';
import HeroSection from './HeroSection.jsx';
import Features from './Features.jsx';
import HowItWorks from './HowItWorks.jsx';
import Footer from './Footer.jsx';
import './LandingPage.css';

const HomePage = () => {
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

export default HomePage;

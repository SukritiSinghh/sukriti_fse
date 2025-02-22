// This file has been renamed to Footer.jsx
import React from 'react';
import { Link } from 'react-router-dom';
import './Footer.css';

const Footer = () => {
  return (
    <footer className="footer">
      <div className="footer-content">
        <div className="footer-section">
          <h4>Quick Links</h4>
          <Link to="/about">About</Link>
          <Link to="/privacy">Privacy Policy</Link>
          <Link to="/terms">Terms & Conditions</Link>
        </div>
        <div className="footer-section">
          <h4>Contact Info</h4>
          <p>Email: contact@insuretech.com</p>
          <p>Phone: +1 (555) 123-4567</p>
          <p>Address: 123 Tech Street, Silicon Valley</p>
        </div>
        <div className="footer-section">
          <h4>Follow Us</h4>
          <div className="social-icons">
            <a href="https://linkedin.com" target="_blank" rel="noopener noreferrer">LinkedIn</a>
            <a href="https://twitter.com" target="_blank" rel="noopener noreferrer">Twitter</a>
            <a href="https://facebook.com" target="_blank" rel="noopener noreferrer">Facebook</a>
          </div>
        </div>
      </div>
      <div className="footer-bottom">
        <p>&copy; 2025 InsureTech. All rights reserved.</p>
      </div>
    </footer>
  );
};

export default Footer;

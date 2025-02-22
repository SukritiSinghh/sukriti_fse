// This file has been renamed to HowItWorks.jsx
import React from 'react';
import './HowItWorks.css';

const HowItWorks = () => {
  const steps = [
    {
      title: 'Sign Up & Join/Create an Organization',
      description: 'Get started by creating your account and organization',
      icon: '1️⃣'
    },
    {
      title: 'Upload Financial Documents',
      description: 'Upload your PDFs & Excel files securely',
      icon: '2️⃣'
    },
    {
      title: 'AI Processes & Analyzes Data',
      description: 'Our AI engine processes and analyzes your data',
      icon: '3️⃣'
    },
    {
      title: 'Get Insights & Manage Risks',
      description: 'Access real-time insights and risk management',
      icon: '4️⃣'
    }
  ];

  return (
    <section className="how-it-works-section">
      <h2>How It Works</h2>
      <div className="steps-container">
        {steps.map((step, index) => (
          <div key={index} className="step-card">
            <div className="step-icon">{step.icon}</div>
            <h3>{step.title}</h3>
            <p>{step.description}</p>
          </div>
        ))}
      </div>
    </section>
  );
};

export default HowItWorks;

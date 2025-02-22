// This file has been renamed to Features.jsx
import React from 'react';
import './Features.css';

const Features = () => {
  const features = [
    {
      title: 'Automated Financial Data Processing',
      description: 'Extracts insights from balance sheets & charge sheets',
      icon: '📊'
    },
    {
      title: 'AI-Powered Risk & Fraud Analysis',
      description: 'Detects anomalies and predicts risks',
      icon: '🔍'
    },
    {
      title: 'Automated Claims Processing',
      description: 'Speeds up insurance claims with AI',
      icon: '⚡'
    },
    {
      title: 'Predictive Analytics for Retention',
      description: 'Helps organizations retain customers',
      icon: '📈'
    }
  ];

  return (
    <section className="features-section">
      <h2>Key Features</h2>
      <div className="features-grid">
        {features.map((feature, index) => (
          <div key={index} className="feature-card">
            <div className="feature-icon">{feature.icon}</div>
            <h3>{feature.title}</h3>
            <p>{feature.description}</p>
          </div>
        ))}
      </div>
    </section>
  );
};

export default Features;

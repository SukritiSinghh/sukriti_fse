// This file has been renamed to NotFoundPage.jsx
import React from 'react';
import { Link } from 'react-router-dom';

const NotFoundPage = () => {
  return (
    <div className="not-found-container">
      <h1>404 - Page Not Found</h1>
      <p>The page you are looking for does not exist.</p>
      <Link to="/" className="home-link">
        Return to Home
      </Link>
    </div>
  );
};

export default NotFoundPage;

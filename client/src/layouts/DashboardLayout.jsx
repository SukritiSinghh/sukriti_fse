import React from 'react';
import { useNavigate } from 'react-router-dom';

const DashboardLayout = ({ children }) => {
  const navigate = useNavigate();

  const handleLogout = () => {
    // Add logout logic here
    navigate('/login');
  };

  return (
    <div className="dashboard-layout">
      <nav className="dashboard-nav">
        <div className="logo">InsureTech</div>
        <div className="nav-links">
          <button onClick={() => navigate('/user-dashboard')}>Dashboard</button>
          <button onClick={() => navigate('/organization-selection')}>Organizations</button>
          <button onClick={handleLogout}>Logout</button>
        </div>
      </nav>
      <div className="dashboard-content">
        {children}
      </div>
    </div>
  );
};

export default DashboardLayout;

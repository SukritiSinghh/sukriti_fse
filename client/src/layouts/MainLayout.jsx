import React from 'react';
import Navbar from '../components/LandingPage/Navbar.jsx';
import Footer from '../components/LandingPage/Footer.jsx';

const MainLayout = ({ children }) => {
  return (
    <div className="main-layout">
      <Navbar />
      <main className="main-content">
        {children}
      </main>
      <Footer />
    </div>
  );
};

export default MainLayout;

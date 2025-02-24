import React, { Suspense, lazy, useState, useEffect } from 'react';
import { Routes, Route, Navigate } from 'react-router-dom';
import DashboardLayout from './layouts/DashboardLayout.jsx';
import LoadingSpinner from './components/common/LoadingSpinner.jsx';
import JoinOrganizationPage from './components/JoinOrganizationPage.jsx';
import OrganizationPage from './components/OrganizationPage.jsx';
import OrganizationSelectionLandingPage from './components/OrganizationSelectionLandingPage.jsx';

// Lazy load components for better performance
const HomePage = lazy(() => import('./components/LandingPage/HomePage.jsx'));
const LoginPage = lazy(() => import('./components/LoginPage.jsx'));
const SignupPage = lazy(() => import('./components/SignupPage.jsx'));
const NotFoundPage = lazy(() => import('./components/NotFoundPage.jsx'));
const Dashboard = lazy(() => import('./components/Dashboard.jsx'));

// Protected Route Component
const ProtectedRoute = ({ children, isAuthenticated }) => {
  if (!isAuthenticated) {
    return <Navigate to="/login" replace />;
  }
  return children;
};

const App = () => {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [hasOrganization, setHasOrganization] = useState(false);

  useEffect(() => {
    // Check if user has an organization whenever authentication status changes
    if (isAuthenticated) {
      const org = localStorage.getItem('organization');
      setHasOrganization(!!org);
    }
  }, [isAuthenticated]);

  return (
    <Suspense fallback={<LoadingSpinner />}>  
      <Routes>
          {/* Public routes */}
          <Route path="/" element={<HomePage />} />

          {/* Auth routes */}
          <Route path="/login" element={<LoginPage setIsAuthenticated={setIsAuthenticated} />} />
          <Route path="/signup" element={<SignupPage setIsAuthenticated={setIsAuthenticated} />} />

          {/* Dashboard route - redirects to org setup if no organization */}
          <Route
            path="/dashboard/*"
            element={
              <Dashboard />
            }
          />
          <Route 
            path="/join-organization" 
            element={
              <ProtectedRoute isAuthenticated={isAuthenticated}>
                <JoinOrganizationPage />
              </ProtectedRoute>
            }
          />
          <Route 
            path="/organization" 
            element={
              <ProtectedRoute isAuthenticated={isAuthenticated}>
                <OrganizationPage />
              </ProtectedRoute>
            }
          />
          <Route 
            path="/organization-selection" 
            element={
              <ProtectedRoute isAuthenticated={isAuthenticated}>
                <OrganizationSelectionLandingPage />
              </ProtectedRoute>
            }
          />

          {/* 404 route */}
          <Route path="*" element={<NotFoundPage />} />
      </Routes>
    </Suspense>
  );
};

export default App;

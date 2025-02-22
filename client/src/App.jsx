import React, { Suspense, lazy } from 'react';
import { Routes, Route, Navigate } from 'react-router-dom';
import DashboardLayout from './layouts/DashboardLayout.jsx';
import LoadingSpinner from './components/common/LoadingSpinner.jsx';

// Lazy load components
const HomePage = lazy(() => import('./components/LandingPage/HomePage.jsx'));
const LoginPage = lazy(() => import('./components/LoginPage.jsx'));
const SignupPage = lazy(() => import('./components/SignupPage.jsx'));
const OrganizationSelectionPage = lazy(() => import('./components/OrganizationSelectionPage.jsx'));
const NotFoundPage = lazy(() => import('./components/NotFoundPage.jsx'));
const DashboardPage = lazy(() => import('./pages/Dashboard.jsx'));

// Protected Route Component
const ProtectedRoute = ({ children, isAuthenticated }) => {
  if (!isAuthenticated) {
    return <Navigate to="/login" replace />;
  }
  return children;
};

const App = () => {
  const isAuthenticated = false; // Replace with your auth logic

  return (
    <Suspense fallback={<LoadingSpinner />}> 
      <Routes>
        {/* Public routes */}
        <Route path="/" element={<HomePage />} />
        <Route path="/login" element={<LoginPage />} />
        <Route path="/signup" element={<SignupPage />} />
        <Route path="/organisationselection" element={<OrganizationSelectionPage />} />

        {/* Protected Dashboard route */}
        <Route
          path="/dashboard"
          element={
            <ProtectedRoute isAuthenticated={isAuthenticated}>
              <DashboardLayout>
                <DashboardPage />
              </DashboardLayout>
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

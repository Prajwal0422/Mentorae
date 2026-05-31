import React from 'react';
import { Routes, Route, Navigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import LoadingSpinner from '../components/common/LoadingSpinner';

// Pages
import LandingPage from '../pages/LandingPage';
import Login from '../pages/auth/Login';
import Signup from '../pages/auth/Signup';
import ForgotPassword from '../pages/auth/ForgotPassword';
import AIMentor from '../pages/AIMentor';
import StudyPlanGenerator from '../components/ai/StudyPlanGenerator';
import RecommendationEngine from '../components/ai/RecommendationEngine';

// Layouts
import DashboardLayout from '../layouts/DashboardLayout';

// Dashboards
import StudentDashboard from '../pages/dashboards/StudentDashboard';

// Protected Route Component
const ProtectedRoute = ({ children }) => {
  const { isAuthenticated, loading } = useAuth();

  if (loading) {
    return <LoadingSpinner fullScreen />;
  }

  return isAuthenticated ? children : <Navigate to="/login" />;
};

const AppRoutes = () => {
  return (
    <Routes>
      {/* Public Routes */}
      <Route path="/" element={<LandingPage />} />
      <Route path="/login" element={<Login />} />
      <Route path="/signup" element={<Signup />} />
      <Route path="/forgot-password" element={<ForgotPassword />} />

      {/* Protected Dashboard Routes */}
      <Route
        path="/dashboard/*"
        element={
          <ProtectedRoute>
            <DashboardLayout />
          </ProtectedRoute>
        }
      >
        <Route path="student" element={<StudentDashboard />} />
        <Route path="ai-mentor" element={<AIMentor />} />
        <Route path="study-plan" element={<StudyPlanGenerator />} />
        <Route path="recommendations" element={<RecommendationEngine />} />
        <Route path="mentor" element={<div className="p-8"><h1 className="text-2xl font-bold">Mentor Dashboard Coming Soon</h1></div>} />
        <Route path="admin" element={<div className="p-8"><h1 className="text-2xl font-bold">Admin Dashboard Coming Soon</h1></div>} />
      </Route>

      {/* Catch all */}
      <Route path="*" element={<Navigate to="/" />} />
    </Routes>
  );
};

export default AppRoutes;

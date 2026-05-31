import React from 'react';
import { NavLink, useNavigate } from 'react-router-dom';
import { motion, AnimatePresence } from 'framer-motion';
import {
  LayoutDashboard,
  Users,
  BookOpen,
  BarChart3,
  Settings,
  LogOut,
  Sparkles,
  X,
  Award,
  Calendar,
  MessageSquare
} from 'lucide-react';
import { useAuth } from '../../context/AuthContext';

const Sidebar = ({ isOpen, onClose }) => {
  const { user, logout } = useAuth();
  const navigate = useNavigate();

  const studentLinks = [
    { to: '/dashboard/student', icon: LayoutDashboard, label: 'Dashboard' },
    { to: '/dashboard/ai-mentor', icon: MessageSquare, label: 'AI Mentor' },
    { to: '/dashboard/student/courses', icon: BookOpen, label: 'My Courses' },
    { to: '/dashboard/student/analytics', icon: BarChart3, label: 'Analytics' },
    { to: '/dashboard/student/calendar', icon: Calendar, label: 'Calendar' },
    { to: '/dashboard/student/achievements', icon: Award, label: 'Achievements' },
  ];

  const mentorLinks = [
    { to: '/dashboard/mentor', icon: LayoutDashboard, label: 'Dashboard' },
    { to: '/dashboard/mentor/students', icon: Users, label: 'My Students' },
    { to: '/dashboard/mentor/analytics', icon: BarChart3, label: 'Analytics' },
    { to: '/dashboard/mentor/messages', icon: MessageSquare, label: 'Messages' },
  ];

  const adminLinks = [
    { to: '/dashboard/admin', icon: LayoutDashboard, label: 'Dashboard' },
    { to: '/dashboard/admin/users', icon: Users, label: 'User Management' },
    { to: '/dashboard/admin/analytics', icon: BarChart3, label: 'System Analytics' },
    { to: '/dashboard/admin/settings', icon: Settings, label: 'Settings' },
  ];

  const links = user?.role === 'admin' ? adminLinks : user?.role === 'mentor' ? mentorLinks : studentLinks;

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  return (
    <>
      {/* Mobile Overlay */}
      <AnimatePresence>
        {isOpen && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            onClick={onClose}
            className="fixed inset-0 bg-black/50 z-40 lg:hidden"
          />
        )}
      </AnimatePresence>

      {/* Sidebar */}
      <motion.aside
        initial={false}
        animate={{ x: isOpen ? 0 : '-100%' }}
        transition={{ type: 'spring', damping: 20 }}
        className={`
          fixed top-0 left-0 z-50 h-full w-64 bg-white shadow-xl
          lg:translate-x-0 lg:static
        `}
      >
        <div className="flex flex-col h-full">
          {/* Logo */}
          <div className="flex items-center justify-between p-6 border-b">
            <div className="flex items-center gap-2">
              <Sparkles className="w-8 h-8 text-primary-600" />
              <span className="text-xl font-bold text-gradient">Mentorae</span>
            </div>
            <button onClick={onClose} className="lg:hidden">
              <X className="w-6 h-6" />
            </button>
          </div>

          {/* User Info */}
          <div className="p-6 border-b">
            <div className="flex items-center gap-3">
              <div className="w-12 h-12 rounded-full bg-gradient-to-br from-primary-500 to-secondary-500 flex items-center justify-center text-white font-bold">
                {user?.avatar || 'U'}
              </div>
              <div>
                <p className="font-semibold text-gray-900">{user?.name || 'User'}</p>
                <p className="text-sm text-gray-600 capitalize">{user?.role || 'Student'}</p>
              </div>
            </div>
          </div>

          {/* Navigation */}
          <nav className="flex-1 p-4 space-y-2 overflow-y-auto">
            {links.map((link) => (
              <NavLink
                key={link.to}
                to={link.to}
                className={({ isActive }) =>
                  `flex items-center gap-3 px-4 py-3 rounded-lg transition-all ${
                    isActive
                      ? 'bg-primary-50 text-primary-700 font-semibold'
                      : 'text-gray-700 hover:bg-gray-100'
                  }`
                }
              >
                <link.icon className="w-5 h-5" />
                <span>{link.label}</span>
              </NavLink>
            ))}
          </nav>

          {/* Bottom Actions */}
          <div className="p-4 border-t space-y-2">
            <NavLink
              to="/settings"
              className="flex items-center gap-3 px-4 py-3 rounded-lg text-gray-700 hover:bg-gray-100 transition-all"
            >
              <Settings className="w-5 h-5" />
              <span>Settings</span>
            </NavLink>
            <button
              onClick={handleLogout}
              className="w-full flex items-center gap-3 px-4 py-3 rounded-lg text-red-600 hover:bg-red-50 transition-all"
            >
              <LogOut className="w-5 h-5" />
              <span>Logout</span>
            </button>
          </div>
        </div>
      </motion.aside>
    </>
  );
};

export default Sidebar;

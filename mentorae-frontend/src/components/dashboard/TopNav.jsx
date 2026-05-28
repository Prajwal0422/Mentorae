import React, { useState } from 'react';
import { Menu, Bell, Search, Bot } from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';
import { notifications } from '../../utils/mockData';

const TopNav = ({ onMenuClick }) => {
  const [showNotifications, setShowNotifications] = useState(false);
  const [showAI, setShowAI] = useState(false);
  const unreadCount = notifications.filter(n => !n.read).length;

  return (
    <header className="sticky top-0 z-30 bg-white border-b border-gray-200 shadow-sm">
      <div className="flex items-center justify-between px-4 py-4 lg:px-8">
        {/* Left Section */}
        <div className="flex items-center gap-4">
          <button
            onClick={onMenuClick}
            className="lg:hidden p-2 hover:bg-gray-100 rounded-lg transition-colors"
          >
            <Menu className="w-6 h-6" />
          </button>

          {/* Search */}
          <div className="hidden md:flex items-center gap-2 bg-gray-100 rounded-lg px-4 py-2 w-96">
            <Search className="w-5 h-5 text-gray-400" />
            <input
              type="text"
              placeholder="Search..."
              className="bg-transparent border-none outline-none w-full text-gray-700"
            />
          </div>
        </div>

        {/* Right Section */}
        <div className="flex items-center gap-4">
          {/* AI Assistant Button */}
          <button
            onClick={() => setShowAI(!showAI)}
            className="relative p-2 hover:bg-primary-50 rounded-lg transition-colors group"
          >
            <Bot className="w-6 h-6 text-gray-700 group-hover:text-primary-600" />
            <span className="absolute -top-1 -right-1 w-2 h-2 bg-green-500 rounded-full animate-pulse" />
          </button>

          {/* Notifications */}
          <div className="relative">
            <button
              onClick={() => setShowNotifications(!showNotifications)}
              className="relative p-2 hover:bg-gray-100 rounded-lg transition-colors"
            >
              <Bell className="w-6 h-6 text-gray-700" />
              {unreadCount > 0 && (
                <span className="absolute -top-1 -right-1 w-5 h-5 bg-red-500 text-white text-xs rounded-full flex items-center justify-center">
                  {unreadCount}
                </span>
              )}
            </button>

            {/* Notifications Dropdown */}
            <AnimatePresence>
              {showNotifications && (
                <motion.div
                  initial={{ opacity: 0, y: 10 }}
                  animate={{ opacity: 1, y: 0 }}
                  exit={{ opacity: 0, y: 10 }}
                  className="absolute right-0 mt-2 w-80 bg-white rounded-xl shadow-2xl border border-gray-200 overflow-hidden"
                >
                  <div className="p-4 border-b bg-gray-50">
                    <h3 className="font-semibold text-gray-900">Notifications</h3>
                  </div>
                  <div className="max-h-96 overflow-y-auto">
                    {notifications.map((notification) => (
                      <div
                        key={notification.id}
                        className={`p-4 border-b hover:bg-gray-50 transition-colors ${
                          !notification.read ? 'bg-blue-50' : ''
                        }`}
                      >
                        <p className="font-medium text-gray-900 text-sm">{notification.title}</p>
                        <p className="text-sm text-gray-600 mt-1">{notification.message}</p>
                        <p className="text-xs text-gray-400 mt-2">{notification.time}</p>
                      </div>
                    ))}
                  </div>
                  <div className="p-3 bg-gray-50 text-center">
                    <button className="text-sm text-primary-600 hover:text-primary-700 font-semibold">
                      View All Notifications
                    </button>
                  </div>
                </motion.div>
              )}
            </AnimatePresence>
          </div>
        </div>
      </div>

      {/* AI Assistant Panel */}
      <AnimatePresence>
        {showAI && (
          <motion.div
            initial={{ opacity: 0, height: 0 }}
            animate={{ opacity: 1, height: 'auto' }}
            exit={{ opacity: 0, height: 0 }}
            className="border-t bg-gradient-to-r from-primary-50 to-secondary-50"
          >
            <div className="p-4 max-w-4xl mx-auto">
              <div className="flex items-start gap-3">
                <div className="w-10 h-10 rounded-full bg-gradient-to-br from-primary-500 to-secondary-500 flex items-center justify-center text-white">
                  <Bot className="w-6 h-6" />
                </div>
                <div className="flex-1">
                  <p className="font-semibold text-gray-900 mb-2">AI Assistant</p>
                  <p className="text-sm text-gray-600 mb-3">
                    Hi! I'm your AI learning assistant. How can I help you today?
                  </p>
                  <div className="flex gap-2 flex-wrap">
                    <button className="px-3 py-1 bg-white rounded-full text-sm hover:bg-gray-100 transition-colors">
                      📊 Show my progress
                    </button>
                    <button className="px-3 py-1 bg-white rounded-full text-sm hover:bg-gray-100 transition-colors">
                      💡 Study tips
                    </button>
                    <button className="px-3 py-1 bg-white rounded-full text-sm hover:bg-gray-100 transition-colors">
                      📚 Recommend resources
                    </button>
                  </div>
                </div>
              </div>
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </header>
  );
};

export default TopNav;

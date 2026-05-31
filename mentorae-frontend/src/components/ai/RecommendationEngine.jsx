import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { Sparkles, BookOpen, Target, TrendingUp, Clock, Award, AlertCircle } from 'lucide-react';
import Button from '../common/Button';
import Card from '../common/Card';
import LoadingSpinner from '../common/LoadingSpinner';

const RecommendationEngine = () => {
  const [loading, setLoading] = useState(false);
  const [recommendations, setRecommendations] = useState(null);
  const [error, setError] = useState('');

  const generateRecommendations = async () => {
    setLoading(true);
    setError('');
    
    try {
      const token = localStorage.getItem('token');
      const response = await fetch('http://localhost:8000/api/ai/recommendations', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify({
          focus_areas: ['weak_subjects', 'attendance', 'study_habits']
        })
      });

      if (!response.ok) throw new Error('Failed to generate recommendations');
      
      const data = await response.json();
      setRecommendations(data.recommendations);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const categoryIcons = {
    'Study Resources': BookOpen,
    'Time Management': Clock,
    'Skill Development': Target,
    'Performance Improvement': TrendingUp,
    'Achievement Goals': Award
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-purple-50 via-white to-blue-50 p-6">
      <div className="max-w-6xl mx-auto">
        {/* Header */}
        <motion.div
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          className="mb-8"
        >
          <div className="flex items-center gap-3 mb-2">
            <div className="p-3 bg-gradient-to-br from-purple-500 to-blue-500 rounded-xl">
              <Sparkles className="w-6 h-6 text-white" />
            </div>
            <h1 className="text-3xl font-bold bg-gradient-to-r from-purple-600 to-blue-600 bg-clip-text text-transparent">
              AI Recommendations
            </h1>
          </div>
          <p className="text-gray-600 ml-16">
            Get personalized recommendations to improve your academic performance
          </p>
        </motion.div>

        {/* Generate Button */}
        {!recommendations && (
          <motion.div
            initial={{ opacity: 0, scale: 0.95 }}
            animate={{ opacity: 1, scale: 1 }}
            className="text-center py-12"
          >
            <Card className="max-w-md mx-auto p-8">
              <div className="mb-6">
                <div className="w-20 h-20 bg-gradient-to-br from-purple-100 to-blue-100 rounded-full flex items-center justify-center mx-auto mb-4">
                  <Sparkles className="w-10 h-10 text-purple-600" />
                </div>
                <h2 className="text-xl font-semibold mb-2">Generate Personalized Recommendations</h2>
                <p className="text-gray-600">
                  Our AI will analyze your profile and provide tailored suggestions
                </p>
              </div>
              <Button
                onClick={generateRecommendations}
                disabled={loading}
                className="w-full"
              >
                {loading ? (
                  <span className="flex items-center justify-center gap-2">
                    <LoadingSpinner size="sm" />
                    Analyzing...
                  </span>
                ) : (
                  'Generate Recommendations'
                )}
              </Button>
            </Card>
          </motion.div>
        )}

        {/* Error Message */}
        {error && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            className="mb-6"
          >
            <Card className="border-red-200 bg-red-50 p-4">
              <div className="flex items-center gap-2 text-red-600">
                <AlertCircle className="w-5 h-5" />
                <span>{error}</span>
              </div>
            </Card>
          </motion.div>
        )}

        {/* Recommendations Display */}
        {recommendations && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            className="space-y-6"
          >
            {/* Summary Card */}
            <Card className="p-6 bg-gradient-to-br from-purple-500 to-blue-500 text-white">
              <h2 className="text-2xl font-bold mb-2">Your Personalized Recommendations</h2>
              <p className="opacity-90">
                Based on your current performance and goals
              </p>
            </Card>

            {/* Recommendations Grid */}
            <div className="grid md:grid-cols-2 gap-6">
              {Object.entries(recommendations).map(([category, items], index) => {
                const Icon = categoryIcons[category] || BookOpen;
                
                return (
                  <motion.div
                    key={category}
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ delay: index * 0.1 }}
                  >
                    <Card className="p-6 h-full hover:shadow-lg transition-shadow">
                      <div className="flex items-center gap-3 mb-4">
                        <div className="p-2 bg-purple-100 rounded-lg">
                          <Icon className="w-5 h-5 text-purple-600" />
                        </div>
                        <h3 className="text-lg font-semibold">{category}</h3>
                      </div>
                      
                      <ul className="space-y-3">
                        {Array.isArray(items) ? (
                          items.map((item, idx) => (
                            <li key={idx} className="flex items-start gap-2">
                              <div className="w-1.5 h-1.5 bg-purple-500 rounded-full mt-2 flex-shrink-0" />
                              <span className="text-gray-700 text-sm">{item}</span>
                            </li>
                          ))
                        ) : (
                          <li className="text-gray-700 text-sm">{items}</li>
                        )}
                      </ul>
                    </Card>
                  </motion.div>
                );
              })}
            </div>

            {/* Action Buttons */}
            <div className="flex gap-4 justify-center pt-4">
              <Button
                variant="outline"
                onClick={() => setRecommendations(null)}
              >
                Generate New
              </Button>
              <Button onClick={generateRecommendations} disabled={loading}>
                {loading ? 'Refreshing...' : 'Refresh Recommendations'}
              </Button>
            </div>
          </motion.div>
        )}
      </div>
    </div>
  );
};

export default RecommendationEngine;

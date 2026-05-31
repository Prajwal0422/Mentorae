import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { Calendar, Plus, X, Loader, Download } from 'lucide-react';
import Button from '../common/Button';
import Card from '../common/Card';
import { generateStudyPlan } from '../../services/aiService';
import ReactMarkdown from 'react-markdown';

const StudyPlanGenerator = () => {
  const [duration, setDuration] = useState(7);
  const [subjects, setSubjects] = useState(['']);
  const [focusAreas, setFocusAreas] = useState(['']);
  const [loading, setLoading] = useState(false);
  const [studyPlan, setStudyPlan] = useState(null);

  const addSubject = () => {
    setSubjects([...subjects, '']);
  };

  const removeSubject = (index) => {
    setSubjects(subjects.filter((_, i) => i !== index));
  };

  const updateSubject = (index, value) => {
    const newSubjects = [...subjects];
    newSubjects[index] = value;
    setSubjects(newSubjects);
  };

  const addFocusArea = () => {
    setFocusAreas([...focusAreas, '']);
  };

  const removeFocusArea = (index) => {
    setFocusAreas(focusAreas.filter((_, i) => i !== index));
  };

  const updateFocusArea = (index, value) => {
    const newFocusAreas = [...focusAreas];
    newFocusAreas[index] = value;
    setFocusAreas(newFocusAreas);
  };

  const handleGenerate = async () => {
    const validSubjects = subjects.filter(s => s.trim());
    const validFocusAreas = focusAreas.filter(f => f.trim());

    if (validSubjects.length === 0) {
      alert('Please add at least one subject');
      return;
    }

    setLoading(true);
    try {
      const data = await generateStudyPlan(
        duration,
        validSubjects,
        validFocusAreas.length > 0 ? validFocusAreas : null
      );

      if (data.success) {
        setStudyPlan(data);
      } else {
        alert(data.error || 'Failed to generate study plan');
      }
    } catch (error) {
      console.error('Error:', error);
      alert('Failed to generate study plan. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const downloadPlan = () => {
    if (!studyPlan) return;

    const blob = new Blob([studyPlan.study_plan], { type: 'text/markdown' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `study-plan-${duration}-days.md`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
  };

  return (
    <div className="space-y-6">
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
      >
        <div className="flex items-center gap-3 mb-6">
          <div className="w-12 h-12 rounded-xl bg-gradient-to-br from-primary-500 to-secondary-500 flex items-center justify-center text-white">
            <Calendar className="w-7 h-7" />
          </div>
          <div>
            <h1 className="text-2xl font-bold text-gray-900">Study Plan Generator</h1>
            <p className="text-gray-600">Create a personalized study schedule</p>
          </div>
        </div>
      </motion.div>

      <div className="grid lg:grid-cols-2 gap-6">
        {/* Input Form */}
        <Card>
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Plan Details</h3>

          {/* Duration */}
          <div className="mb-6">
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Plan Duration
            </label>
            <select
              value={duration}
              onChange={(e) => setDuration(Number(e.target.value))}
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
            >
              <option value={7}>7 Days (1 Week)</option>
              <option value={14}>14 Days (2 Weeks)</option>
              <option value={30}>30 Days (1 Month)</option>
              <option value={60}>60 Days (2 Months)</option>
              <option value={90}>90 Days (3 Months)</option>
            </select>
          </div>

          {/* Subjects */}
          <div className="mb-6">
            <div className="flex items-center justify-between mb-2">
              <label className="block text-sm font-medium text-gray-700">
                Subjects
              </label>
              <button
                onClick={addSubject}
                className="text-primary-600 hover:text-primary-700 text-sm flex items-center gap-1"
              >
                <Plus className="w-4 h-4" />
                Add Subject
              </button>
            </div>
            <div className="space-y-2">
              {subjects.map((subject, index) => (
                <div key={index} className="flex gap-2">
                  <input
                    type="text"
                    value={subject}
                    onChange={(e) => updateSubject(index, e.target.value)}
                    placeholder="e.g., Data Structures"
                    className="flex-1 px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
                  />
                  {subjects.length > 1 && (
                    <button
                      onClick={() => removeSubject(index)}
                      className="p-2 text-red-600 hover:bg-red-50 rounded-lg"
                    >
                      <X className="w-5 h-5" />
                    </button>
                  )}
                </div>
              ))}
            </div>
          </div>

          {/* Focus Areas */}
          <div className="mb-6">
            <div className="flex items-center justify-between mb-2">
              <label className="block text-sm font-medium text-gray-700">
                Focus Areas (Optional)
              </label>
              <button
                onClick={addFocusArea}
                className="text-primary-600 hover:text-primary-700 text-sm flex items-center gap-1"
              >
                <Plus className="w-4 h-4" />
                Add Focus Area
              </button>
            </div>
            <div className="space-y-2">
              {focusAreas.map((area, index) => (
                <div key={index} className="flex gap-2">
                  <input
                    type="text"
                    value={area}
                    onChange={(e) => updateFocusArea(index, e.target.value)}
                    placeholder="e.g., Binary Trees"
                    className="flex-1 px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
                  />
                  <button
                    onClick={() => removeFocusArea(index)}
                    className="p-2 text-red-600 hover:bg-red-50 rounded-lg"
                  >
                    <X className="w-5 h-5" />
                  </button>
                </div>
              ))}
            </div>
          </div>

          <Button
            onClick={handleGenerate}
            loading={loading}
            className="w-full"
            icon={<Calendar className="w-5 h-5" />}
          >
            Generate Study Plan
          </Button>
        </Card>

        {/* Generated Plan */}
        <Card className="lg:col-span-1">
          <div className="flex items-center justify-between mb-4">
            <h3 className="text-lg font-semibold text-gray-900">Your Study Plan</h3>
            {studyPlan && (
              <Button
                variant="outline"
                size="sm"
                onClick={downloadPlan}
                icon={<Download className="w-4 h-4" />}
              >
                Download
              </Button>
            )}
          </div>

          {loading ? (
            <div className="flex flex-col items-center justify-center py-12">
              <Loader className="w-12 h-12 text-primary-600 animate-spin mb-4" />
              <p className="text-gray-600">Generating your personalized study plan...</p>
            </div>
          ) : studyPlan ? (
            <div className="prose prose-sm max-w-none">
              <ReactMarkdown>{studyPlan.study_plan}</ReactMarkdown>
            </div>
          ) : (
            <div className="text-center py-12 text-gray-500">
              <Calendar className="w-16 h-16 mx-auto mb-4 text-gray-300" />
              <p>Fill in the details and click "Generate Study Plan"</p>
              <p className="text-sm mt-2">Your personalized plan will appear here</p>
            </div>
          )}
        </Card>
      </div>
    </div>
  );
};

export default StudyPlanGenerator;

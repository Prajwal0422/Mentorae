import React, { useState, useRef, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { 
  Send, 
  Bot, 
  User, 
  Sparkles, 
  BookOpen, 
  Calendar,
  Lightbulb,
  Loader,
  History,
  Trash2
} from 'lucide-react';
import ReactMarkdown from 'react-markdown';
import Card from '../components/common/Card';
import Button from '../components/common/Button';
import { useAuth } from '../context/AuthContext';
import { sendChatMessage, getChatHistory } from '../services/aiService';

const AIMentor = () => {
  const { user } = useAuth();
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const [showHistory, setShowHistory] = useState(false);
  const [conversationId] = useState(`conv_${Date.now()}`);
  const messagesEndRef = useRef(null);

  const suggestedPrompts = [
    { icon: <BookOpen className="w-4 h-4" />, text: "Explain recursion in simple terms" },
    { icon: <Calendar className="w-4 h-4" />, text: "Create a 7-day study plan for my exams" },
    { icon: <Lightbulb className="w-4 h-4" />, text: "How can I improve my CGPA?" },
    { icon: <Sparkles className="w-4 h-4" />, text: "Give me personalized study recommendations" },
  ];

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  useEffect(() => {
    // Load chat history
    loadChatHistory();
  }, []);

  const loadChatHistory = async () => {
    try {
      const data = await getChatHistory(20);
      if (data.success && data.history.length > 0) {
        // Convert history to messages format
        const historyMessages = data.history.reverse().map(item => ([
          { role: 'user', content: item.message, timestamp: item.timestamp },
          { role: 'assistant', content: item.response, timestamp: item.timestamp }
        ])).flat();
        
        setMessages(historyMessages);
      } else {
        // Welcome message if no history
        setWelcomeMessage();
      }
    } catch (error) {
      console.error('Error loading history:', error);
      setWelcomeMessage();
    }
  };

  const setWelcomeMessage = () => {
    setMessages([
      {
        role: 'assistant',
        content: `Hello ${user?.full_name || 'there'}! 👋 I'm your AI Academic Mentor. I'm here to help you with:\n\n- Explaining complex concepts\n- Creating personalized study plans\n- Providing learning strategies\n- Recommending resources\n- Improving your academic performance\n\nHow can I assist you today?`,
        timestamp: new Date().toISOString()
      }
    ]);
  };

  const clearHistory = () => {
    setMessages([]);
    setWelcomeMessage();
  };

  const handleSend = async () => {
    if (!input.trim() || loading) return;

    const userMessage = {
      role: 'user',
      content: input,
      timestamp: new Date().toISOString()
    };

    setMessages(prev => [...prev, userMessage]);
    setInput('');
    setLoading(true);

    try {
      const data = await sendChatMessage(input, conversationId);

      if (data.success) {
        const assistantMessage = {
          role: 'assistant',
          content: data.response,
          timestamp: data.timestamp
        };

        setMessages(prev => [...prev, assistantMessage]);
      } else {
        throw new Error(data.error || 'Failed to get response');
      }
    } catch (error) {
      console.error('Error:', error);
      
      // Mock response for demo
      const mockResponse = {
        role: 'assistant',
        content: `I understand you're asking about "${input}". Let me help you with that.\n\nThis is a demonstration response. In production, this would be powered by AI to provide personalized academic guidance based on your profile.\n\n**Key Points:**\n1. Personalized to your academic level\n2. Considers your weak subjects\n3. Tailored to your learning style\n\nWould you like me to elaborate on any specific aspect?`,
        timestamp: new Date().toISOString()
      };

      setMessages(prev => [...prev, mockResponse]);
    } finally {
      setLoading(false);
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  const handleSuggestedPrompt = (prompt) => {
    setInput(prompt);
  };

  return (
    <div className="h-[calc(100vh-8rem)] flex flex-col">
      {/* Header */}
      <motion.div
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
        className="mb-6"
      >
        <div className="flex items-center gap-3 mb-2">
          <div className="w-12 h-12 rounded-xl bg-gradient-to-br from-primary-500 to-secondary-500 flex items-center justify-center text-white">
            <Bot className="w-7 h-7" />
          </div>
          <div>
            <h1 className="text-2xl font-bold text-gray-900">AI Academic Mentor</h1>
            <p className="text-gray-600">Your personal learning assistant</p>
          </div>
          <div className="ml-auto flex gap-2">
            <Button
              variant="ghost"
              size="sm"
              onClick={() => setShowHistory(!showHistory)}
              icon={<History className="w-4 h-4" />}
            >
              History
            </Button>
            <Button
              variant="ghost"
              size="sm"
              onClick={clearHistory}
              icon={<Trash2 className="w-4 h-4" />}
            >
              Clear
            </Button>
          </div>
        </div>
      </motion.div>

      {/* Chat Container */}
      <Card className="flex-1 flex flex-col overflow-hidden p-0">
        {/* Messages */}
        <div className="flex-1 overflow-y-auto p-6 space-y-4">
          <AnimatePresence>
            {messages.map((message, index) => (
              <motion.div
                key={index}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0 }}
                className={`flex gap-3 ${message.role === 'user' ? 'justify-end' : 'justify-start'}`}
              >
                {message.role === 'assistant' && (
                  <div className="w-8 h-8 rounded-full bg-gradient-to-br from-primary-500 to-secondary-500 flex items-center justify-center text-white flex-shrink-0">
                    <Bot className="w-5 h-5" />
                  </div>
                )}
                
                <div
                  className={`max-w-[70%] rounded-2xl p-4 ${
                    message.role === 'user'
                      ? 'bg-primary-600 text-white'
                      : 'bg-gray-100 text-gray-900'
                  }`}
                >
                  {message.role === 'assistant' ? (
                    <div className="prose prose-sm max-w-none">
                      <ReactMarkdown>{message.content}</ReactMarkdown>
                    </div>
                  ) : (
                    <p className="whitespace-pre-wrap">{message.content}</p>
                  )}
                </div>

                {message.role === 'user' && (
                  <div className="w-8 h-8 rounded-full bg-gradient-to-br from-gray-600 to-gray-700 flex items-center justify-center text-white flex-shrink-0">
                    <User className="w-5 h-5" />
                  </div>
                )}
              </motion.div>
            ))}
          </AnimatePresence>

          {loading && (
            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              className="flex gap-3"
            >
              <div className="w-8 h-8 rounded-full bg-gradient-to-br from-primary-500 to-secondary-500 flex items-center justify-center text-white">
                <Bot className="w-5 h-5" />
              </div>
              <div className="bg-gray-100 rounded-2xl p-4">
                <div className="flex items-center gap-2">
                  <Loader className="w-4 h-4 animate-spin text-primary-600" />
                  <span className="text-gray-600">Thinking...</span>
                </div>
              </div>
            </motion.div>
          )}

          <div ref={messagesEndRef} />
        </div>

        {/* Suggested Prompts */}
        {messages.length === 1 && (
          <div className="px-6 pb-4">
            <p className="text-sm text-gray-600 mb-3">Try asking:</p>
            <div className="grid grid-cols-2 gap-2">
              {suggestedPrompts.map((prompt, index) => (
                <button
                  key={index}
                  onClick={() => handleSuggestedPrompt(prompt.text)}
                  className="flex items-center gap-2 p-3 bg-gray-50 hover:bg-gray-100 rounded-lg text-left text-sm transition-colors"
                >
                  {prompt.icon}
                  <span className="text-gray-700">{prompt.text}</span>
                </button>
              ))}
            </div>
          </div>
        )}

        {/* Input Area */}
        <div className="border-t p-4">
          <div className="flex gap-2">
            <textarea
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyPress={handleKeyPress}
              placeholder="Ask me anything about your studies..."
              className="flex-1 px-4 py-3 border border-gray-300 rounded-lg resize-none focus:ring-2 focus:ring-primary-500 focus:border-transparent"
              rows="1"
              style={{ minHeight: '48px', maxHeight: '120px' }}
            />
            <Button
              onClick={handleSend}
              disabled={!input.trim() || loading}
              icon={<Send className="w-5 h-5" />}
              className="px-6"
            >
              Send
            </Button>
          </div>
          <p className="text-xs text-gray-500 mt-2">
            Press Enter to send, Shift+Enter for new line
          </p>
        </div>
      </Card>
    </div>
  );
};

export default AIMentor;

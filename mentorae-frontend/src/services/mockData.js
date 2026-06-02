// Mock data for charts and analytics

export const studentPerformanceData = [
  { month: 'Jan', gpa: 3.2, attendance: 85, assignments: 90 },
  { month: 'Feb', gpa: 3.4, attendance: 88, assignments: 92 },
  { month: 'Mar', gpa: 3.6, attendance: 90, assignments: 95 },
  { month: 'Apr', gpa: 3.5, attendance: 87, assignments: 88 },
  { month: 'May', gpa: 3.7, attendance: 92, assignments: 94 },
  { month: 'Jun', gpa: 3.8, attendance: 95, assignments: 96 },
];

export const subjectPerformance = [
  { subject: 'Mathematics', score: 85, average: 75 },
  { subject: 'Physics', score: 78, average: 72 },
  { subject: 'Chemistry', score: 92, average: 80 },
  { subject: 'Computer Science', score: 95, average: 85 },
  { subject: 'English', score: 88, average: 82 },
];

export const attendanceData = [
  { name: 'Present', value: 85, color: '#10b981' },
  { name: 'Absent', value: 10, color: '#ef4444' },
  { name: 'Late', value: 5, color: '#f59e0b' },
];

export const weeklyActivity = [
  { day: 'Mon', hours: 4 },
  { day: 'Tue', hours: 6 },
  { day: 'Wed', hours: 5 },
  { day: 'Thu', hours: 7 },
  { day: 'Fri', hours: 5 },
  { day: 'Sat', hours: 3 },
  { day: 'Sun', hours: 2 },
];

export const recentActivities = [
  {
    id: 1,
    type: 'assignment',
    title: 'Submitted Data Structures Assignment',
    time: '2 hours ago',
    icon: '📝',
  },
  {
    id: 2,
    type: 'grade',
    title: 'Received grade for Physics Quiz',
    time: '5 hours ago',
    icon: '🎯',
  },
  {
    id: 3,
    type: 'message',
    title: 'New message from Prof. Johnson',
    time: '1 day ago',
    icon: '💬',
  },
  {
    id: 4,
    type: 'achievement',
    title: 'Earned "Perfect Attendance" badge',
    time: '2 days ago',
    icon: '🏆',
  },
];

export const aiRecommendations = [
  {
    id: 1,
    title: 'Focus on Calculus',
    description: 'Your performance in calculus has dropped by 12%. Consider reviewing chapters 5-7.',
    priority: 'high',
    icon: '📊',
  },
  {
    id: 2,
    title: 'Great Progress in CS',
    description: 'You\'re excelling in Computer Science. Keep up the excellent work!',
    priority: 'low',
    icon: '💻',
  },
  {
    id: 3,
    title: 'Upcoming Deadline',
    description: 'Physics lab report due in 3 days. Start early to ensure quality work.',
    priority: 'medium',
    icon: '⏰',
  },
];

export const mentorStudents = [
  {
    id: 1,
    name: 'Alice Johnson',
    gpa: 3.8,
    attendance: 95,
    risk: 'low',
    lastContact: '2 days ago',
    avatar: 'AJ',
  },
  {
    id: 2,
    name: 'Bob Smith',
    gpa: 2.9,
    attendance: 78,
    risk: 'high',
    lastContact: '1 week ago',
    avatar: 'BS',
  },
  {
    id: 3,
    name: 'Carol Williams',
    gpa: 3.5,
    attendance: 88,
    risk: 'medium',
    lastContact: '3 days ago',
    avatar: 'CW',
  },
  {
    id: 4,
    name: 'David Brown',
    gpa: 3.9,
    attendance: 97,
    risk: 'low',
    lastContact: '1 day ago',
    avatar: 'DB',
  },
];

export const departmentStats = [
  { department: 'Computer Science', students: 450, avgGPA: 3.6 },
  { department: 'Engineering', students: 380, avgGPA: 3.4 },
  { department: 'Business', students: 320, avgGPA: 3.5 },
  { department: 'Arts', students: 280, avgGPA: 3.7 },
  { department: 'Sciences', students: 410, avgGPA: 3.5 },
];

export const systemAnalytics = [
  { metric: 'Total Users', value: 2450, change: '+12%', trend: 'up' },
  { metric: 'Active Students', value: 1850, change: '+8%', trend: 'up' },
  { metric: 'Active Mentors', value: 145, change: '+5%', trend: 'up' },
  { metric: 'Avg Session Time', value: '45min', change: '+15%', trend: 'up' },
];

export const notifications = [
  {
    id: 1,
    title: 'New Assignment Posted',
    message: 'Dr. Smith posted a new assignment in Data Structures',
    time: '10 minutes ago',
    read: false,
    type: 'assignment',
  },
  {
    id: 2,
    title: 'Grade Updated',
    message: 'Your grade for Physics Midterm has been updated',
    time: '1 hour ago',
    read: false,
    type: 'grade',
  },
  {
    id: 3,
    title: 'Mentor Session Reminder',
    message: 'You have a mentoring session tomorrow at 2 PM',
    time: '3 hours ago',
    read: true,
    type: 'reminder',
  },
];

export const testimonials = [
  {
    id: 1,
    name: 'Sarah Johnson',
    role: 'Computer Science Student',
    content: 'Mentorae has transformed how I track my academic progress. The AI recommendations are incredibly helpful!',
    avatar: 'SJ',
    rating: 5,
  },
  {
    id: 2,
    name: 'Prof. Michael Chen',
    role: 'Academic Mentor',
    content: 'As a mentor, this platform makes it easy to identify students who need support and track their progress effectively.',
    avatar: 'MC',
    rating: 5,
  },
  {
    id: 3,
    name: 'Emily Rodriguez',
    role: 'Engineering Student',
    content: 'The analytics and insights have helped me improve my GPA by 0.5 points in just one semester!',
    avatar: 'ER',
    rating: 5,
  },
];

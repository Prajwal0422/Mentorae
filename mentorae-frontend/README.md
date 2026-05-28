# Mentorae Frontend

Modern, production-level React frontend for the Mentorae AI-Powered Student Intelligence & Mentorship Platform.

## 🚀 Tech Stack

- **React 18** - Modern React with hooks
- **Tailwind CSS** - Utility-first CSS framework
- **Framer Motion** - Smooth animations
- **Recharts** - Beautiful data visualizations
- **React Router** - Client-side routing
- **Lucide React** - Modern icon library
- **Axios** - HTTP client

## 📁 Project Structure

```
src/
├── components/          # Reusable UI components
│   ├── common/         # Generic components (Button, Card, Input, etc.)
│   └── dashboard/      # Dashboard-specific components
├── layouts/            # Layout components
├── pages/              # Page components
│   ├── auth/          # Authentication pages
│   └── dashboards/    # Dashboard pages
├── routes/            # Routing configuration
├── context/           # React Context providers
├── utils/             # Utility functions and mock data
├── hooks/             # Custom React hooks
├── services/          # API services
├── assets/            # Static assets
└── animations/        # Animation configurations
```

## 🎨 Features

### Landing Page
- Modern hero section with gradient animations
- Feature showcase cards
- Statistics section
- Testimonials
- Responsive footer
- Call-to-action sections

### Authentication
- Login page
- Signup page with role selection
- Forgot password flow
- Protected routes

### Student Dashboard
- GPA and attendance tracking
- Performance trend charts
- Subject-wise analytics
- AI-powered recommendations
- Recent activity timeline
- Attendance breakdown
- Achievement tracking

### UI/UX Features
- Glassmorphism effects
- Smooth animations with Framer Motion
- Responsive design (mobile, tablet, desktop)
- Loading states
- Hover effects
- Modern card layouts
- Gradient backgrounds
- Custom scrollbars

## 🛠️ Installation

```bash
# Install dependencies
npm install

# Start development server
npm start

# Build for production
npm run build
```

## 🎯 Available Scripts

- `npm start` - Run development server (http://localhost:3000)
- `npm run build` - Create production build
- `npm test` - Run tests
- `npm run eject` - Eject from Create React App

## 🔐 Authentication Flow

1. User lands on homepage
2. Clicks "Get Started" or "Login"
3. Enters credentials
4. Redirected to role-specific dashboard
5. Protected routes ensure authentication

## 📊 Dashboard Features

### Student Dashboard
- **Performance Analytics**: Line charts showing GPA and attendance trends
- **Subject Performance**: Bar charts comparing scores with class average
- **Attendance Breakdown**: Pie chart visualization
- **AI Recommendations**: Personalized suggestions based on performance
- **Recent Activity**: Timeline of academic activities
- **Quick Stats**: GPA, Attendance, Assignments, Achievements

### Mentor Dashboard (Coming Soon)
- Student performance overview
- Risk alerts
- Mentorship tracking
- Comparison charts

### Admin Dashboard (Coming Soon)
- Total users statistics
- System analytics
- Department overview
- User management

## 🎨 Design System

### Colors
- **Primary**: Blue (#0ea5e9)
- **Secondary**: Purple (#d946ef)
- **Success**: Green (#10b981)
- **Warning**: Yellow (#f59e0b)
- **Danger**: Red (#ef4444)

### Components
- Reusable Button component with variants
- Card component with glass effect option
- Input component with icons and validation
- Loading spinner with full-screen option
- Stat cards with trend indicators

## 📱 Responsive Breakpoints

- **Mobile**: < 768px
- **Tablet**: 768px - 1024px
- **Desktop**: > 1024px

## 🔄 State Management

- React Context API for authentication
- Local state with useState
- Mock data for development

## 🚀 Deployment

```bash
# Build production bundle
npm run build

# Deploy to hosting service
# (Vercel, Netlify, AWS S3, etc.)
```

## 📝 Environment Variables

Create a `.env` file in the root:

```env
REACT_APP_API_URL=http://localhost:5500
REACT_APP_ENV=development
```

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open Pull Request

## 📄 License

MIT License - see LICENSE file for details

## 👥 Team

Built with ❤️ by the Mentorae Team

## 🔗 Links

- [Backend Repository](../AI-tutor)
- [Documentation](./docs)
- [Live Demo](#)

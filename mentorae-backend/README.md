# Mentorae Backend API

Production-ready FastAPI backend for the Mentorae AI-Powered Student Intelligence & Mentorship Platform.

## 🚀 Tech Stack

- **FastAPI** - Modern, fast web framework
- **MongoDB Atlas** - Cloud database
- **Motor** - Async MongoDB driver
- **JWT** - JSON Web Token authentication
- **Passlib** - Password hashing with bcrypt
- **Pydantic** - Data validation
- **Python-dotenv** - Environment management

## 📁 Project Structure

```
app/
├── config/              # Configuration and database setup
│   ├── __init__.py
│   ├── settings.py     # Environment settings
│   └── database.py     # MongoDB connection
├── models/              # Database models
│   ├── __init__.py
│   └── user.py         # User, Student, Mentor models
├── schemas/             # Pydantic schemas (request/response)
│   ├── __init__.py
│   └── user.py         # User schemas
├── routes/              # API endpoints
│   ├── __init__.py
│   ├── auth.py         # Authentication routes
│   ├── student.py      # Student routes
│   ├── mentor.py       # Mentor routes
│   └── admin.py        # Admin routes
├── services/            # Business logic
│   ├── __init__.py
│   └── auth_service.py # Authentication service
├── middleware/          # Custom middleware
│   ├── __init__.py
│   └── logging.py      # Request logging
├── dependencies/        # FastAPI dependencies
│   ├── __init__.py
│   └── auth.py         # Auth dependencies
├── utils/               # Utility functions
│   ├── __init__.py
│   └── security.py     # Password & JWT utilities
├── __init__.py
└── main.py             # Application entry point
```

## 🔐 Authentication & Authorization

### User Roles
- **Student** - Access to personal dashboard and performance data
- **Mentor** - Access to assigned students and mentoring tools
- **Admin** - Full system access and user management

### JWT Authentication
- Token-based authentication
- 30-minute token expiration (configurable)
- Role-based access control (RBAC)
- Protected routes with dependency injection

## 📚 API Endpoints

### Authentication (`/api/auth`)
- `POST /register` - Register new user
- `POST /login` - Login and get JWT token
- `GET /me` - Get current user profile
- `PUT /me` - Update user profile
- `POST /change-password` - Change password
- `POST /logout` - Logout user

### Student Routes (`/api/student`) 🔒
- `GET /dashboard` - Student dashboard data
- `GET /courses` - Enrolled courses
- `GET /performance` - Academic performance
- `GET /assignments` - Assignments and submissions
- `GET /ai-recommendations` - AI-powered recommendations

### Mentor Routes (`/api/mentor`) 🔒
- `GET /dashboard` - Mentor dashboard
- `GET /students` - Assigned students list
- `GET /students/{id}` - Student details
- `GET /analytics` - Student analytics
- `POST /sessions` - Create mentoring session

### Admin Routes (`/api/admin`) 🔒
- `GET /dashboard` - System dashboard
- `GET /users` - All users list
- `GET /users/{id}` - User details
- `PUT /users/{id}/activate` - Activate user
- `PUT /users/{id}/deactivate` - Deactivate user
- `GET /analytics` - System analytics
- `DELETE /users/{id}` - Delete user

🔒 = Requires authentication

## 🛠️ Installation & Setup

### Prerequisites
- Python 3.8+
- MongoDB Atlas account (or local MongoDB)
- pip or poetry

### 1. Clone Repository
```bash
cd mentorae-backend
```

### 2. Create Virtual Environment
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Environment Configuration
Create `.env` file in the root directory:

```env
# MongoDB Configuration
MONGODB_URL=mongodb+srv://username:password@cluster.mongodb.net/
DATABASE_NAME=mentorae_db

# JWT Configuration
SECRET_KEY=your-super-secret-key-change-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Application Configuration
APP_NAME=Mentorae API
APP_VERSION=1.0.0
DEBUG=True
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:5173

# Server Configuration
HOST=0.0.0.0
PORT=8000
```

### 5. Run Application
```bash
# Development mode (with auto-reload)
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Or using Python
python -m app.main
```

### 6. Access API Documentation
- **Swagger UI**: http://localhost:8000/api/docs
- **ReDoc**: http://localhost:8000/api/redoc
- **OpenAPI JSON**: http://localhost:8000/api/openapi.json

## 🔑 MongoDB Collections

### users
```json
{
  "_id": "ObjectId",
  "email": "string",
  "hashed_password": "string",
  "full_name": "string",
  "role": "student|mentor|admin",
  "is_active": "boolean",
  "is_verified": "boolean",
  "avatar": "string",
  "phone": "string",
  "created_at": "datetime",
  "updated_at": "datetime",
  "last_login": "datetime"
}
```

### students
```json
{
  "_id": "ObjectId",
  "user_id": "ObjectId",
  "student_id": "string",
  "department": "string",
  "year": "integer",
  "semester": "integer",
  "gpa": "float",
  "attendance_percentage": "float",
  "mentor_id": "ObjectId",
  "courses": ["string"],
  "achievements": ["string"],
  "created_at": "datetime",
  "updated_at": "datetime"
}
```

### mentors
```json
{
  "_id": "ObjectId",
  "user_id": "ObjectId",
  "employee_id": "string",
  "department": "string",
  "specialization": "string",
  "experience_years": "integer",
  "students": ["ObjectId"],
  "max_students": "integer",
  "bio": "string",
  "created_at": "datetime",
  "updated_at": "datetime"
}
```

## 🧪 Testing

### Manual Testing with cURL

**Register User:**
```bash
curl -X POST "http://localhost:8000/api/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "student@example.com",
    "password": "SecurePass123",
    "full_name": "John Doe",
    "role": "student"
  }'
```

**Login:**
```bash
curl -X POST "http://localhost:8000/api/auth/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=student@example.com&password=SecurePass123"
```

**Access Protected Route:**
```bash
curl -X GET "http://localhost:8000/api/student/dashboard" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

## 🔒 Security Features

- **Password Hashing**: Bcrypt with salt
- **JWT Tokens**: Secure token generation
- **CORS**: Configurable origins
- **Input Validation**: Pydantic schemas
- **SQL Injection**: Protected by Motor/MongoDB
- **Rate Limiting**: Ready for implementation
- **HTTPS**: Recommended for production

## 📊 Future Enhancements

The architecture supports easy integration of:

- ✅ AI Mentor Assistant
- ✅ RAG Chatbot
- ✅ Student Analytics
- ✅ Performance Prediction
- ✅ Report Generation
- ✅ Real-time Notifications
- ✅ File Upload/Storage
- ✅ Email Verification
- ✅ Password Reset
- ✅ OAuth Integration

## 🚀 Deployment

### Docker Deployment
```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Environment Variables for Production
```env
DEBUG=False
SECRET_KEY=use-strong-random-key-here
MONGODB_URL=your-production-mongodb-url
ALLOWED_ORIGINS=https://yourdomain.com
```

## 📝 API Response Format

### Success Response
```json
{
  "message": "Success message",
  "data": { }
}
```

### Error Response
```json
{
  "detail": "Error message"
}
```

### Token Response
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "user": {
    "_id": "507f1f77bcf86cd799439011",
    "email": "user@example.com",
    "full_name": "John Doe",
    "role": "student"
  }
}
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

## 📞 Support

For issues and questions:
- GitHub Issues
- Email: support@mentorae.com
- Documentation: /api/docs

---

**Note**: This is a production-ready backend with proper authentication, authorization, and scalable architecture. Ready for integration with the React frontend and future AI features.

# AI Mentor Module

The AI Mentor module powers Mentorae's intelligent academic guidance system using Google Gemini Pro.

## Features

- **Contextual Chat** — answers academic questions personalised to the student's CGPA, semester, attendance, and weak subjects
- **Study Plan Generator** — creates day-by-day study plans (7-day, 30-day, exam prep)
- **Recommendation Engine** — generates targeted improvement strategies and resource suggestions
- **Chat History** — persists all conversations in MongoDB for continuity

## Endpoints

| Method | Path | Description |
|--------|------|-------------|
| POST | `/api/ai/chat` | Chat with AI mentor |
| POST | `/api/ai/study-plan` | Generate a study plan |
| POST | `/api/ai/recommendations` | Get personalised recommendations |
| GET | `/api/ai/history` | Retrieve chat history |
| GET | `/api/ai/status` | Check AI service availability |

All endpoints require a valid JWT token (`Authorization: Bearer <token>`).

## Setup

1. Add your Gemini API key to `.env`:
   ```
   GEMINI_API_KEY=your_key_here
   ```

2. Install the dependency:
   ```
   pip install google-generativeai
   ```

## Architecture

```
app/ai/
├── gemini_client.py     # Gemini API wrapper with retry logic
├── mentor_service.py    # Business logic and MongoDB persistence
├── prompt_templates.py  # Structured prompts for each feature
└── routes/
    └── ai.py            # FastAPI route handlers
```

## Example Request

```bash
curl -X POST http://localhost:8000/api/ai/chat \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{"message": "Explain recursion with an example"}'
```

## Future Enhancements

- RAG (Retrieval-Augmented Generation) with course materials
- Streaming responses via WebSocket
- Performance prediction model integration
- Multi-turn conversation memory

# Mentorae Setup Guide

## Prerequisites

- Python 3.8 or higher
- Ollama (for embeddings)
- Google Gemini API key
- SerpAPI key

## Installation Steps

### 1. Clone the Repository
```bash
git clone https://github.com/Prajwal0422/Mentorae.git
cd Mentorae
```

### 2. Install Python Dependencies
```bash
pip install -r AI-tutor/requirements.txt
```

### 3. Install Ollama
Download and install Ollama from [https://ollama.ai](https://ollama.ai)

Pull the embedding model:
```bash
ollama pull mxbai-embed-large:latest
```

### 4. Configure Environment Variables
Create a `.env` file in the root directory:
```bash
cp .env.example .env
```

Edit `.env` and add your API keys:
- Get Google Gemini API key from [Google AI Studio](https://makersuite.google.com/app/apikey)
- Get SerpAPI key from [SerpAPI](https://serpapi.com/)

### 5. Run the Application

#### CLI Mode
```bash
python AI-tutor/aiFeatures/python/ai_assistant.py
```

#### Web Interface
```bash
python AI-tutor/testFrontend/FlaskApp/app.py
```

Then open your browser to `http://localhost:5500`

## Features

- **Text Chat**: Ask questions via text input
- **Voice Interaction**: Speech-to-text and text-to-speech
- **PDF Upload**: Upload documents for RAG-based answers
- **Web Search**: Automatic web scraping for current information

## Troubleshooting

### PyAudio Installation Issues
**Windows**: Download the wheel file from [here](https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyaudio)
**Linux**: `sudo apt-get install portaudio19-dev python3-pyaudio`
**Mac**: `brew install portaudio`

### Ollama Connection Issues
Ensure Ollama is running: `ollama serve`

# Sziget Chatbot

Sziget-inspired chatbot project built with an Angular frontend and a lightweight Python backend.

The goal of the project is to present a festival-style landing page and an interactive chat experience where visitors can ask questions about the Sziget Festival, such as tickets, lineup, camping, rules, vibe, and extra programs.

## What the project does

- shows a Sziget-themed landing page
- introduces the chatbot with explanation sections
- displays clickable topic cards with sample questions
- lets the user start chatting immediately from the frontend
- serves answers from a Python knowledge base
- works as a simple guest-chat flow without login

## Main features

### Frontend

- Angular-based landing page and chat UI
- Sziget-inspired visual style
- topic cards loaded from backend data
- clickable sample questions that fill the chat input
- preview/sample conversation mode
- responsive layout with mobile support
- subtle animations for sections and mascot areas

### Backend

- Python API with Flask
- knowledge base driven answers
- theme/category listing endpoint
- guest chat endpoint
- lightweight matching engine for festival-related questions

## Project structure

```text
sziget-chatbot/
├── public/                      # Static assets
├── src/                         # Angular frontend source
│   └── app/
│       ├── models/
│       ├── pages/
│       └── services/
├── sziget-backend/              # Python backend
│   ├── app.py
│   ├── chatbot_engine.py
│   ├── knowledge_base.py
│   └── requirements.txt
├── package.json
└── angular.json
```

## Requirements

### Frontend

- Node.js
- npm

### Backend

- Python 3.11+ recommended
- pip

Note:
The backend in this repo was adjusted to avoid heavy ML build dependencies, so it can run more easily on a typical Windows setup as well.

## Install

### 1. Frontend dependencies

From the project root:

```powershell
cd C:\xampp\htdocs\SzigetAI\sziget-chatbot
npm install
```

### 2. Backend dependencies

```powershell
cd C:\xampp\htdocs\SzigetAI\sziget-chatbot\sziget-backend
python -m pip install -r requirements.txt
```

## Run the project

### Start the backend

```powershell
cd C:\xampp\htdocs\SzigetAI\sziget-chatbot\sziget-backend
python app.py
```

Backend URL:

- [http://127.0.0.1:8000/api/health](http://127.0.0.1:8000/api/health)

### Start the frontend

Open a new terminal:

```powershell
cd C:\xampp\htdocs\SzigetAI\sziget-chatbot
npm start -- --host 127.0.0.1 --port 4200
```

Frontend URL:

- [http://127.0.0.1:4200](http://127.0.0.1:4200)

## Available API endpoints

### `GET /api/health`

Simple health check endpoint.

### `GET /api/themes`

Returns the available frontend topic categories and sample questions.

### `POST /api/guest-chat`

Handles guest chat messages.

Example request body:

```json
{
  "message": "Mennyibe kerül egy napijegy?",
  "messages": []
}
```

## Current topic groups

The frontend is currently built around these backend themes:

- `festival_info`
- `pricing`
- `camping`
- `rules`
- `general`
- `lineup_schedule`
- `programs`

## Frontend summary

The frontend was designed to help users understand quickly:

- what the chatbot is for
- what kinds of questions it can answer
- why it is useful even if someone could search manually
- how to start interacting without friction

The page is structured more like a festival campaign landing page than a standard chat app.

## Build

To build the Angular frontend:

```powershell
cd C:\xampp\htdocs\SzigetAI\sziget-chatbot
npm run build
```

## Notes

- The project currently focuses on guest chat usage.
- The answer quality depends on the knowledge base entries in `sziget-backend/knowledge_base.py`.
- If you expand the knowledge base, the frontend topic cards can reflect those themes through the backend endpoint.

## Suggested next improvements

- richer theme browsing in the frontend
- fuller backend knowledge base coverage
- improved chat memory/history handling
- better production startup scripts
- deployment-ready configuration

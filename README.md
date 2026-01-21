# Weekly Planner

A web application that allows for a weekly plan, built with FastAPI and Angular.

## Features

- 🗣️ Week display with tasks
- 📁 Add/ edit/ remove tasks

## Prerequisites

- Python 3.10+
- Node.js 18+
- OpenAI API key and/or Anthropic API key
- 'gh' github cli
- astral uv

## Setup

### 1. Install Dependencies

```bash
# Backend
cd app/server
uv sync --all-extras

# Frontend
cd app/client
npm install
```

## Quick Start

Use the provided script to start both services:

```bash
./scripts/start.sh
```

Press `Ctrl+C` to stop both services.

The script will:

- Check that `.env` exists in `app/server/`
- Start the backend on http://localhost:5173
- Start the frontend on http://localhost:4200
- Handle graceful shutdown when you exit

## Manual Start (Alternative)

### Backend

```bash
cd app/server
# .env is loaded automatically by python-dotenv
uv run python server.py
```

### Frontend

```bash
cd app/client
npm run start
```

## Usage

1. **Add task**: Click "Add task" to Add a new task
2. **Edit task**:
3. **Delete task**:
4. **Clear week**:

## Development

### Backend Commands

```bash
cd app/server
uv run python server.py      # Start server with hot reload
uv run pytest               # Run tests
uv add <package>            # Add package to project
uv remove <package>         # Remove package from project
uv sync --all-extras        # Sync all extras
```

### Frontend Commands

```bash
cd app/client
npm run start              # Start dev server (Angular)
npm run build              # Build for production
npm run test               # Run tests
```

## Project Structure

```
.
├── app/                    # Main application
│   ├── client/             # Angular frontend
│   └── server/             # FastAPI backend
│
├── adws/                   # AI Developer Workflows - Core agent system
├── scripts/                # Utility scripts (start.sh, stop_apps.sh)
├── specs/                  # Feature specifications
├── agents/                 # Agent execution logging
└── logs/                   # Structured session logs
```

## ADWs

- `uv run adws/health_check.py` - Basic health check ADW
- `uv run adws/trigger_webhook.py` - React to incoming webhook trigger (be sure to setup a tunnel and your github webhook)
- `uv run adws/trigger_cron.py` - Simple cron job trigger that checks github issues every N seconds
- `uv run adws/adw_plan_build.py` - Plan -> Build AI Developer Workflow (ADW)

## API Endpoints

- `POST /api/tasks` - Add a task
- `PATCH /api/task/:id` - Edit a task
- `GET /api/tasks` - Get week tasks
- `GET /api/health` - Health check

## Troubleshooting

**Backend won't start:**

- Check Python version: `python --version` (requires 3.12+)
- Verify API keys are set: `echo $OPENAI_API_KEY`

**Frontend errors:**

- Clear node_modules: `rm -rf node_modules && npm install`
- Check Node version: `node --version` (requires 18+)

**CORS issues:**

- Ensure backend is running on port 5173
- Frontend should be on port 4200
- Check CORS configuration in server.py

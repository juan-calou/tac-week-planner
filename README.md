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

## Vercel Deployment

This project supports separate deployments for the client and server on Vercel.

### Prerequisites

1. Install Vercel CLI:
   ```bash
   npm install -g vercel
   ```

2. Login to Vercel:
   ```bash
   vercel login
   ```

### Deploy Server (Backend)

1. Navigate to the server directory:
   ```bash
   cd app/server
   ```

2. Deploy to Vercel:
   ```bash
   vercel
   ```

3. For production deployment:
   ```bash
   vercel --prod
   ```

4. Set environment variables in Vercel dashboard or via CLI:
   ```bash
   vercel env add OPENAI_API_KEY
   vercel env add ANTHROPIC_API_KEY
   vercel env add ALLOWED_ORIGINS
   ```

   For `ALLOWED_ORIGINS`, use your client URL (e.g., `https://your-client-app.vercel.app`)

5. After deployment, note the server URL (e.g., `https://your-server-app.vercel.app`)

### Deploy Client (Frontend)

1. Navigate to the client directory:
   ```bash
   cd app/client
   ```

2. Update the production environment file:
   Edit `src/environments/environment.prod.ts` and replace the API URL with your deployed server URL:
   ```typescript
   export const environment = {
     production: true,
     apiUrl: 'https://your-server-app.vercel.app/api'
   };
   ```

3. Deploy to Vercel:
   ```bash
   vercel
   ```

4. For production deployment:
   ```bash
   vercel --prod
   ```

### Connect Client and Server

After both deployments:

1. Update the server's `ALLOWED_ORIGINS` environment variable with your client URL:
   ```bash
   cd app/server
   vercel env add ALLOWED_ORIGINS production
   # Enter: https://your-client-app.vercel.app
   ```

2. Redeploy the server to apply the changes:
   ```bash
   vercel --prod
   ```

### Verify Deployment

1. Visit your client URL (e.g., `https://your-client-app.vercel.app`)
2. Test the API connection by adding, editing, or deleting tasks
3. Check the Network tab in browser DevTools to verify API requests are working

### Environment Variables Reference

**Server (`app/server`):**
- `OPENAI_API_KEY` - OpenAI API key for AI features
- `ANTHROPIC_API_KEY` - Anthropic API key for AI features
- `ALLOWED_ORIGINS` - Comma-separated list of allowed origins (your client URL)

**Client (`app/client`):**
- API URL is configured in `src/environments/environment.prod.ts`

### Useful Vercel CLI Commands

```bash
vercel --help              # Show all commands
vercel ls                  # List all deployments
vercel domains             # Manage custom domains
vercel env ls              # List environment variables
vercel logs                # View deployment logs
vercel remove [deployment] # Remove a specific deployment
```

## Project Structure

```
.
├── app/                    # Main application
│   ├── client/             # Angular frontend
│   │   └── vercel.json    # Vercel configuration for client
│   └── server/             # FastAPI backend
│       └── vercel.json    # Vercel configuration for server
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

# Installation Guide

This guide explains how to set up and run **Enterprise MCP Platform** for local development.

---

# Prerequisites

Ensure the following software is installed before you begin.

| Software | Recommended Version |
|-----------|---------------------|
| Git | Latest |
| Python | 3.11+ |
| Node.js | 20+ |
| npm | 10+ |
| Docker Desktop | Latest |
| Docker Compose | Latest |
| VS Code (Optional) | Latest |

Verify your installation:

```bash
python --version
node --version
npm --version
docker --version
docker compose version
git --version
```

---

# Clone the Repository

Clone the repository from GitHub.

```bash
git clone https://github.com/<your-username>/enterprise-mcp-platform.git
```

Move into the project directory.

```bash
cd enterprise-mcp-platform
```

---

# Project Structure

```text
enterprise-mcp-platform/
├── ai-gateway/
├── frontend/
├── infrastructure/
├── mcp-servers/
├── monitoring/
├── docs/
├── tests/
└── docker-compose.yml
```

---

# Environment Variables

Create a `.env` file in the `ai-gateway/` directory.

Example:

```env
OPENAI_API_KEY=your_openai_api_key

OPENAI_MODEL=gpt-4.1-mini

HOST=0.0.0.0
PORT=8000

LOG_LEVEL=INFO

ENABLE_METRICS=true
ENABLE_TRACING=true
```

> **Important:** Never commit `.env` files to version control.

---

# Backend Setup

Navigate to the backend.

```bash
cd ai-gateway
```

Create a virtual environment.

### Windows

```bash
python -m venv .venv

.venv\Scripts\activate
```

### macOS / Linux

```bash
python -m venv .venv

source .venv/bin/activate
```

Install dependencies.

```bash
pip install -r requirements.txt
```

Run the backend.

```bash
uvicorn app.main:app --reload
```

Backend URL:

```
http://localhost:8000
```

API documentation:

```
http://localhost:8000/docs
```

---

# Frontend Setup

Open another terminal.

```bash
cd frontend
```

Install dependencies.

```bash
npm install
```

Start the development server.

```bash
npm run dev
```

Frontend URL:

```
http://localhost:3000
```

---

# Docker Installation

The easiest way to run the complete platform is with Docker Compose.

From the project root:

```bash
docker compose up --build
```

Run in detached mode:

```bash
docker compose up -d
```

Stop the services:

```bash
docker compose down
```

Rebuild containers:

```bash
docker compose up --build
```

---

# Monitoring

When monitoring is enabled, the following services are available:

| Service | URL |
|---------|-----|
| AI Gateway | http://localhost:8000 |
| API Docs | http://localhost:8000/docs |
| Frontend | http://localhost:3000 |
| Prometheus | http://localhost:9090 |
| Grafana | http://localhost:3001 |

---

# Verify the Installation

Check the backend health endpoint.

```bash
curl http://localhost:8000/health
```

Expected response:

```json
{
  "status": "healthy"
}
```

Open the frontend in your browser:

```
http://localhost:3000
```

Verify that:

- Backend starts successfully
- Frontend loads correctly
- API documentation is accessible
- Docker containers are healthy (if using Docker)
- Monitoring dashboards are available

---

# Running Tests

Backend:

```bash
pytest
```

Frontend:

```bash
npm test
```

---

# Updating Dependencies

Backend:

```bash
pip install --upgrade -r requirements.txt
```

Frontend:

```bash
npm update
```

---

# Troubleshooting

## Port Already in Use

If a port is already occupied, stop the conflicting process or update the port configuration.

---

## Docker Issues

Rebuild all containers:

```bash
docker compose down

docker compose up --build
```

Remove unused Docker resources:

```bash
docker system prune -f
```

---

## Python Dependency Errors

Upgrade `pip` and reinstall dependencies.

```bash
python -m pip install --upgrade pip

pip install -r requirements.txt
```

---

## Node.js Dependency Errors

Remove existing dependencies and reinstall.

```bash
rm -rf node_modules
rm package-lock.json

npm install
```

On Windows:

```powershell
rmdir /s /q node_modules
del package-lock.json

npm install
```

---

# Next Steps

After completing the installation:

1. Configure your environment variables.
2. Explore the API documentation at `/docs`.
3. Review the project architecture in `docs/architecture.md`.
4. Learn the repository layout in `docs/project-structure.md`.
5. Run the test suite to verify your setup.

---
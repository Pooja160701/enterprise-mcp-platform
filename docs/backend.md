# Backend Guide

This document describes the backend architecture, core components, and development workflow for the **Enterprise MCP Platform**.

---

# Overview

The backend is built using **FastAPI** and serves as the orchesation layer between the frontend, AI models, MCP servers, and supporting platform services.

Its primary responsibilities include:

- REST API
- AI request processing
- MCP server communication
- Tool execution
- Plugin management
- Governance and policy enforcement
- Memory management
- Observability
- Monitoring

---

# Technology Stack

| Technology | Purpose |
|------------|---------|
| Python 3.11+ | Programming Language |
| FastAPI | Web Framework |
| Uvicorn | ASGI Server |
| Pydantic | Validation & Configuration |
| OpenAI API | AI Model Integration |
| Prometheus | Metrics |
| OpenTelemetry | Distributed Tracing |
| Docker | Containerization |

---

# Backend Architecture

```
                Frontend
                    │
                    ▼
          FastAPI API Endpoints
                    │
                    ▼
             Service Layer
                    │
     ┌──────────────┼──────────────┐
     ▼              ▼              ▼
 Planner      Tool Selection   Governance
     │              │              │
     └──────────────┼──────────────┘
                    ▼
             Plugin Manager
                    │
                    ▼
               MCP Core
                    │
                    ▼
             External MCP Servers
```

---

# Directory Structure

```text
ai-gateway/

├── app/
│   ├── api/
│   ├── approval/
│   ├── core/
│   ├── db/
│   ├── governance/
│   ├── hybrid_search/
│   ├── memory/
│   ├── observability/
│   ├── parallel/
│   ├── planner/
│   ├── plugins/
│   ├── reasoning/
│   ├── schemas/
│   ├── services/
│   ├── tool_selection/
│   ├── main.py
│   └── ...
├── requirements.txt
├── Dockerfile
└── .env
```

---

# API Layer

Located in:

```text
app/api/
```

Responsibilities:

- Request validation
- Response serialization
- Authentication (future)
- Routing
- Error handling

Typical endpoints include:

- `/health`
- `/chat`
- `/tools`
- `/servers`
- `/mcp/status`

---

# Service Layer

Located in:

```text
app/services/
```

Contains the application's business logic.

Examples:

- AI orchestration
- Conversation management
- Tool execution
- Context handling
- Response aggregation

API routes should remain lightweight and delegate business logic to this layer.

---

# Planner

Located in:

```text
app/planner/
```

Responsibilities:

- Execution planning
- Dependency analysis
- Retry handling
- Timeout management
- Parallel task scheduling

---

# Tool Selection

Located in:

```text
app/tool_selection/
```

Responsibilities:

- Capability matching
- Intent classification
- Tool ranking
- Confidence scoring
- Fallback selection

---

# Memory

Located in:

```text
app/memory/
```

Provides contextual awareness across conversations.

Features include:

- Session memory
- Conversation history
- Long-term memory
- Context ranking
- Memory retrieval

---

# Governance

Located in:

```text
app/governance/
```

Enterprise governance ensures secure and policy-compliant execution.

Capabilities include:

- RBAC
- Policy enforcement
- Secret protection
- Tool permissions
- Compliance validation
- Rate limiting

---

# Plugin System

Located in:

```text
app/plugins/
```

The plugin system enables extensibility without modifying the platform core.

Responsibilities:

- Plugin discovery
- Dynamic loading
- Registration
- Version management
- Sandbox execution

---

# MCP Integration

The backend communicates with external MCP servers through the MCP Core.

Workflow:

```
API Request
      │
      ▼
Planner
      │
      ▼
Plugin Manager
      │
      ▼
MCP Core
      │
      ▼
MCP Server
      │
      ▼
External Tool
```

---

# Observability

Located in:

```text
app/observability/
```

Provides platform visibility through:

- Structured logging
- Prometheus metrics
- OpenTelemetry tracing
- Request monitoring
- Error tracking

Metrics include:

- API latency
- Request count
- Error rate
- Tool execution time
- Active sessions

---

# Configuration

Configuration is managed using environment variables.

Example:

```env
OPENAI_API_KEY=your_api_key
OPENAI_MODEL=gpt-4.1-mini

HOST=0.0.0.0
PORT=8000

LOG_LEVEL=INFO

ENABLE_METRICS=true
ENABLE_TRACING=true
```

Refer to `docs/configuration.md` for a complete list of supported settings.

---

# Running the Backend

Create and activate a virtual environment.

Windows:

```bash
python -m venv .venv
.venv\Scripts\activate
```

macOS / Linux:

```bash
python -m venv .venv
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Start the server:

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

# Error Handling

The backend returns structured JSON error responses.

Example:

```json
{
  "detail": "Tool not found."
}
```

Use appropriate HTTP status codes for client and server errors.

---

# Testing

Run the backend test suite:

```bash
pytest
```

Recommended test categories:

- Unit tests
- Integration tests
- API endpoint tests
- Plugin tests
- Governance tests

---

# Logging

Logging should be:

- Structured
- Consistent
- Context-aware

Avoid logging:

- API keys
- Passwords
- Access tokens
- Sensitive user data

---

# Performance Best Practices

- Prefer asynchronous endpoints.
- Reuse HTTP clients where possible.
- Validate input early.
- Keep services modular.
- Avoid blocking operations.
- Cache repeated computations when appropriate.

---

# Security Best Practices

- Validate all incoming requests.
- Sanitize user input.
- Store secrets in environment variables.
- Apply least-privilege principles.
- Enable HTTPS in production.
- Keep dependencies up to date.
- Restrict access to trusted MCP servers.

---

# Troubleshooting

## Backend does not start

Verify:

- Python version
- Virtual environment activation
- Installed dependencies
- Environment variables

---

## OpenAI connection issues

Check:

- `OPENAI_API_KEY`
- Internet connectivity
- API quota and permissions

---

## MCP server unavailable

Verify:

- Server is running.
- Connection settings are correct.
- Network access is available.

---

## Import errors

Reinstall dependencies:

```bash
pip install -r requirements.txt
```

Confirm the correct Python environment is active.

---
# API Reference

This document provides an overview of the REST API exposed by the **Enterprise MCP Platform**.

The backend is implemented using **FastAPI** and provides endpoints for AI interactions, MCP server management, platform monitoring, and system health.

---

# Base URL

Local Development

```
http://localhost:8000
```

Production

```
https://your-domain.com
```

---

# Interactive API Documentation

FastAPI automatically generates interactive API documentation.

| Documentation | URL |
|---------------|-----|
| Swagger UI | `/docs` |
| ReDoc | `/redoc` |

Examples:

```
http://localhost:8000/docs
```

```
http://localhost:8000/redoc
```

---

# API Conventions

## Content Type

All requests should use:

```
Content-Type: application/json
```

Responses are returned as JSON.

---

## HTTP Status Codes

| Status | Description |
|----------|-------------|
| 200 | Success |
| 201 | Resource Created |
| 400 | Invalid Request |
| 401 | Unauthorized |
| 403 | Forbidden |
| 404 | Resource Not Found |
| 422 | Validation Error |
| 429 | Too Many Requests |
| 500 | Internal Server Error |

---

# Health API

## GET /health

Returns the current health status of the platform.

### Request

```http
GET /health
```

### Response

```json
{
  "status": "healthy"
}
```

---

# Chat API

## POST /chat

Processes a user request through the AI Gateway.

### Request

```json
{
  "message": "List all available MCP servers."
}
```

### Response

```json
{
  "response": "The following MCP servers are available..."
}
```

---

# MCP Status API

## GET /mcp/status

Returns the current MCP connection status.

### Response

```json
{
  "connected": true,
  "servers": [
    {
      "name": "github",
      "status": "connected"
    }
  ]
}
```

---

# MCP Tools API

## GET /mcp/tools

Returns all discovered tools from connected MCP servers.

### Response

```json
{
  "tools": [
    {
      "name": "list_repositories",
      "server": "github",
      "description": "List GitHub repositories"
    }
  ]
}
```

---

# MCP Servers API

## GET /servers

Returns all registered MCP servers.

### Response

```json
[
  {
    "name": "github",
    "status": "connected"
  },
  {
    "name": "docker",
    "status": "connected"
  }
]
```

---

# Tool Execution API

## POST /tools/execute

Executes a tool exposed by an MCP server.

### Request

```json
{
  "server": "github",
  "tool": "list_repositories",
  "arguments": {}
}
```

### Response

```json
{
  "success": true,
  "result": [
    {
      "name": "enterprise-mcp-platform"
    }
  ]
}
```

---

# Monitoring API

## GET /metrics

Returns Prometheus-compatible metrics.

Example:

```
# HELP http_requests_total
# TYPE http_requests_total counter
```

---

# Error Response Format

Errors are returned in a consistent JSON structure.

Example:

```json
{
  "detail": "Tool not found."
}
```

Validation errors:

```json
{
  "detail": [
    {
      "loc": [
        "body",
        "message"
      ],
      "msg": "Field required",
      "type": "missing"
    }
  ]
}
```

---

# Authentication

Authentication is planned for a future release.

Expected mechanisms include:

- JWT access tokens
- API keys
- Role-Based Access Control (RBAC)

---

# Rate Limiting

Future releases may include configurable rate limiting.

Example:

```
100 requests per minute
```

---

# Request Flow

```
Client
   │
   ▼
FastAPI Router
   │
   ▼
Validation
   │
   ▼
Service Layer
   │
   ▼
Planner
   │
   ▼
Tool Selection
   │
   ▼
Governance
   │
   ▼
Plugin Manager
   │
   ▼
MCP Core
   │
   ▼
MCP Server
```

---

# Example Using curl

Health endpoint:

```bash
curl http://localhost:8000/health
```

Chat request:

```bash
curl -X POST http://localhost:8000/chat \
-H "Content-Type: application/json" \
-d '{
  "message":"Hello"
}'
```

---

# Example Using Python

```python
import requests

response = requests.post(
    "http://localhost:8000/chat",
    json={
        "message": "Hello"
    }
)

print(response.json())
```

---

# Example Using JavaScript

```javascript
const response = await fetch("http://localhost:8000/chat", {
  method: "POST",
  headers: {
    "Content-Type": "application/json"
  },
  body: JSON.stringify({
    message: "Hello"
  })
});

const data = await response.json();

console.log(data);
```

---

# API Versioning

Future API versions will follow semantic versioning.

Example:

```
/api/v1/
/api/v2/
```

Backward compatibility will be maintained whenever possible.

---

# Best Practices

- Validate all input.
- Use HTTPS in production.
- Handle errors gracefully.
- Keep requests idempotent where appropriate.
- Avoid exposing sensitive information in responses.
- Document any new endpoints before merging.

---
# Troubleshooting Guide

This document provides solutions to common issues encountered while developing, deploying, and running the **Enterprise MCP Platform**.

If your issue is not covered here, please check the project logs, review the documentation, or open a GitHub issue.

---

# Quick Diagnostics

Before troubleshooting a specific problem, verify the following:

- Git is installed.
- Python 3.11 or later is installed.
- Node.js is installed.
- Docker Desktop is running.
- Required environment variables are configured.
- The backend starts successfully.
- The frontend loads successfully.
- The `/health` endpoint returns a healthy status.

---

# Installation Issues

## Python Dependencies Fail to Install

### Symptoms

```
ModuleNotFoundError

pip install failed
```

### Solution

Upgrade pip:

```bash
python -m pip install --upgrade pip
```

Reinstall dependencies:

```bash
pip install -r requirements.txt
```

---

## Node.js Dependencies Fail

### Symptoms

```
npm ERR!

Cannot resolve dependency
```

### Solution

Delete dependencies:

Linux/macOS:

```bash
rm -rf node_modules package-lock.json
```

Windows:

```powershell
rmdir /s /q node_modules

del package-lock.json
```

Reinstall:

```bash
npm install
```

---

# Backend Issues

## Backend Does Not Start

### Symptoms

```
Error loading ASGI app
```

### Solution

Verify:

- Virtual environment is activated.
- Dependencies are installed.
- `uvicorn` is installed.
- Environment variables are configured.

Run:

```bash
uvicorn app.main:app --reload
```

---

## OpenAI API Errors

### Symptoms

```
Authentication failed

401 Unauthorized
```

### Solution

Check:

- `OPENAI_API_KEY`
- API quota
- Internet connection
- Model name

Example:

```env
OPENAI_API_KEY=your_api_key

OPENAI_MODEL=gpt-4.1-mini
```

---

## Health Endpoint Returns an Error

Verify the backend is running:

```bash
curl http://localhost:8000/health
```

Expected response:

```json
{
  "status": "healthy"
}
```

---

# Frontend Issues

## Frontend Does Not Load

Check:

```bash
npm install

npm run dev
```

Verify:

- Backend is running.
- `NEXT_PUBLIC_API_URL` is correct.
- Port 3000 is available.

---

## API Requests Fail

Check:

- Backend URL
- CORS configuration
- Network connectivity
- Browser developer tools
- Backend logs

---

## Build Errors

Run:

```bash
npm run build
```

Fix any TypeScript or ESLint errors before deployment.

---

# Docker Issues

## Containers Fail to Start

Inspect container status:

```bash
docker compose ps
```

View logs:

```bash
docker compose logs
```

---

## Docker Build Fails

Rebuild without cache:

```bash
docker compose build --no-cache
```

---

## Port Already in Use

Check which process is using the port.

Linux/macOS:

```bash
lsof -i :8000
```

Windows:

```powershell
netstat -ano | findstr :8000
```

Stop the conflicting process or change the port configuration.

---

# MCP Issues

## MCP Server Not Connected

Verify:

- Server is running.
- Transport configuration is correct.
- Required environment variables are set.
- Network connectivity is available.

---

## Tool Discovery Fails

Check:

- MCP server registration.
- Tool definitions.
- Startup logs.
- Plugin configuration.

---

## Tool Execution Times Out

Possible causes:

- Slow external service.
- Network issues.
- Timeout configuration too low.
- Unresponsive MCP server.

Increase timeout if necessary.

---

# Plugin Issues

## Plugin Not Loaded

Verify:

- Plugin exists in the configured directory.
- Required metadata is present.
- Dependencies are installed.
- Plugin is enabled.

---

## Plugin Initialization Error

Review:

- Application logs.
- Plugin configuration.
- Environment variables.
- Version compatibility.

---

# Monitoring Issues

## Metrics Missing

Verify:

```
GET /metrics
```

Check:

- Metrics are enabled.
- Prometheus is scraping the backend.
- Monitoring configuration.

---

## Grafana Dashboard Empty

Verify:

- Grafana is running.
- Prometheus data source is configured.
- Metrics endpoint is accessible.

---

## Missing Traces

Check:

- Tracing enabled.
- OpenTelemetry configuration.
- Trace exporter.

---

# Deployment Issues

## Kubernetes Pods Crash

Inspect:

```bash
kubectl describe pod <pod-name>
```

Logs:

```bash
kubectl logs <pod-name>
```

---

## Docker Deployment Fails

Review:

```bash
docker compose logs
```

Verify:

- Environment variables.
- Docker images.
- Network configuration.

---

# Performance Issues

## Slow API Responses

Possible causes:

- External MCP server latency.
- High CPU usage.
- Excessive logging.
- Network congestion.

Monitor:

- Prometheus metrics.
- Grafana dashboards.
- Application logs.

---

## High Memory Usage

Check:

- Long-running requests.
- Large responses.
- Memory leaks.
- Concurrent request limits.

---

# Logging

Backend logs:

```bash
docker compose logs ai-gateway
```

Frontend logs:

```bash
docker compose logs frontend
```

Follow logs:

```bash
docker compose logs -f
```

---

# Useful Commands

Backend:

```bash
uvicorn app.main:app --reload
```

Frontend:

```bash
npm run dev
```

Docker:

```bash
docker compose up

docker compose down

docker compose logs

docker compose ps
```

Kubernetes:

```bash
kubectl get pods

kubectl get services

kubectl logs <pod-name>
```

---

# Collecting Diagnostic Information

Before reporting an issue, gather:

- Operating system
- Python version
- Node.js version
- Docker version
- Backend logs
- Frontend logs
- Error messages
- Steps to reproduce
- Screenshots (if applicable)

---

# Reporting Issues

When opening a GitHub issue, include:

- Problem description
- Expected behavior
- Actual behavior
- Steps to reproduce
- Relevant logs
- Environment details

This information helps maintainers reproduce and resolve issues more efficiently.

---
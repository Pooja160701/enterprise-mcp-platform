# Docker Guide

This document explains how to build, run, and manage **Enterprise MCP Platform** using Docker and Docker Compose.

---

# Overview

The project is fully containerized to provide a consistent development and deployment environment.

Docker is used for:

- AI Gateway
- Frontend
- Prometheus
- Grafana
- Supporting services

Docker Compose orchestrates all services with a single command.

---

# Prerequisites

Install the following:

| Software | Version |
|-----------|---------|
| Docker Desktop | Latest |
| Docker Compose | Latest |

Verify your installation:

```bash
docker --version
docker compose version
```

---

# Project Structure

```text
enterprise-mcp-platform/

├── docker-compose.yml
├── ai-gateway/
│   └── Dockerfile
├── frontend/
│   └── Dockerfile
├── monitoring/
│   ├── prometheus/
│   └── grafana/
└── infrastructure/
```

---

# Services

The default Docker Compose setup starts the following services.

| Service | Port |
|----------|------|
| AI Gateway | 8000 |
| Frontend | 3000 |
| Prometheus | 9090 |
| Grafana | 3001 |

---

# Build the Project

From the project root:

```bash
docker compose build
```

Rebuild after dependency changes:

```bash
docker compose build --no-cache
```

---

# Start the Platform

Run all services:

```bash
docker compose up
```

Run in detached mode:

```bash
docker compose up -d
```

View running containers:

```bash
docker compose ps
```

---

# Stop the Platform

Stop all services:

```bash
docker compose down
```

Remove containers and networks:

```bash
docker compose down --volumes
```

---

# Viewing Logs

Show logs for all services:

```bash
docker compose logs
```

Follow logs in real time:

```bash
docker compose logs -f
```

View logs for a specific service:

```bash
docker compose logs ai-gateway

docker compose logs frontend

docker compose logs prometheus

docker compose logs grafana
```

---

# Restart Services

Restart all services:

```bash
docker compose restart
```

Restart a specific service:

```bash
docker compose restart ai-gateway
```

---

# Execute Commands Inside Containers

Open a shell in the backend container:

```bash
docker compose exec ai-gateway bash
```

Open a shell in the frontend container:

```bash
docker compose exec frontend sh
```

---

# Environment Variables

Docker Compose loads configuration from the backend `.env` file.

Example:

```yaml
services:
  ai-gateway:
    env_file:
      - ai-gateway/.env
```

Never commit secrets or API keys to the repository.

---

# Persistent Data

By default, Docker volumes are used to preserve service data between container restarts.

Examples include:

- Grafana dashboards
- Prometheus metrics (optional)
- Application data (if configured)

List volumes:

```bash
docker volume ls
```

Remove unused volumes:

```bash
docker volume prune
```

---

# Health Checks

Verify the backend:

```bash
curl http://localhost:8000/health
```

Expected response:

```json
{
  "status": "healthy"
}
```

Verify the frontend:

```
http://localhost:3000
```

Verify Prometheus:

```
http://localhost:9090
```

Verify Grafana:

```
http://localhost:3001
```

---

# Common Docker Commands

| Task | Command |
|------|---------|
| Build images | `docker compose build` |
| Start services | `docker compose up` |
| Start in background | `docker compose up -d` |
| Stop services | `docker compose down` |
| View logs | `docker compose logs` |
| Restart services | `docker compose restart` |
| List containers | `docker compose ps` |
| Remove unused resources | `docker system prune -f` |

---

# Troubleshooting

## Port Already in Use

If Docker reports that a port is already in use:

1. Stop the conflicting process.
2. Update the port mapping in `docker-compose.yml`.
3. Restart the containers.

---

## Container Fails to Start

Inspect container logs:

```bash
docker compose logs ai-gateway
```

Verify:

- Environment variables
- Mounted volumes
- Dockerfile configuration
- Application startup logs

---

## Image Build Fails

Rebuild without cache:

```bash
docker compose build --no-cache
```

---

## Dependency Issues

Rebuild the affected image:

```bash
docker compose up --build
```

---

## Remove All Project Containers

```bash
docker compose down --volumes --remove-orphans
```

---

# Production Recommendations

For production deployments:

- Use multi-stage Docker builds.
- Run containers as a non-root user.
- Pin base image versions.
- Scan images for vulnerabilities.
- Set CPU and memory limits.
- Use restart policies.
- Store secrets securely.
- Use HTTPS behind a reverse proxy.
- Keep images up to date.

---

# Security

Recommended tools:

- Trivy
- Docker Scout
- GitHub Dependabot
- GitHub CodeQL

Regularly scan container images and update dependencies to address known vulnerabilities.

---
# Configuration Guide

This document explains how to configure **Enterprise MCP Platform** for local development, testing, and production deployments.

---

# Configuration Overview

The platform uses **environment variables** for configuration. This approach keeps sensitive information out of the source code and makes deployments portable across different environments.

Configuration includes:

- Application settings
- OpenAI integration
- Server configuration
- Logging
- Monitoring
- Plugin management
- MCP settings
- Security
- Performance tuning

---

# Configuration Files

The following files are commonly used.

```text
enterprise-mcp-platform/

├── .env.example
├── docker-compose.yml
├── ai-gateway/
│   ├── .env
│   └── app/
│       └── core/
│           └── config.py
└── frontend/
```

---

# Environment Variables

Create an `.env` file inside the `ai-gateway/` directory.

Example:

```env
######################################
# OpenAI
######################################

OPENAI_API_KEY=your_api_key
OPENAI_MODEL=gpt-4.1-mini

######################################
# Server
######################################

HOST=0.0.0.0
PORT=8000
DEBUG=true

######################################
# Logging
######################################

LOG_LEVEL=INFO

######################################
# Monitoring
######################################

ENABLE_METRICS=true
ENABLE_TRACING=true

######################################
# MCP
######################################

MCP_TIMEOUT=30
MCP_MAX_CONNECTIONS=20

######################################
# Plugins
######################################

PLUGIN_AUTO_DISCOVERY=true
PLUGIN_DIRECTORY=plugins

######################################
# Performance
######################################

MAX_CONCURRENT_REQUESTS=100
REQUEST_TIMEOUT=60
```

---

# OpenAI Configuration

| Variable | Description | Default |
|-----------|-------------|---------|
| `OPENAI_API_KEY` | API key used to access OpenAI models | Required |
| `OPENAI_MODEL` | Default model used for chat completions | `gpt-4.1-mini` |

---

# Server Configuration

| Variable | Description | Default |
|-----------|-------------|---------|
| `HOST` | Server bind address | `0.0.0.0` |
| `PORT` | Backend port | `8000` |
| `DEBUG` | Enable debug mode | `false` |

---

# Logging Configuration

| Variable | Description | Default |
|-----------|-------------|---------|
| `LOG_LEVEL` | Logging level | `INFO` |

Supported values:

- DEBUG
- INFO
- WARNING
- ERROR
- CRITICAL

---

# Monitoring Configuration

| Variable | Description | Default |
|-----------|-------------|---------|
| `ENABLE_METRICS` | Enable Prometheus metrics | `true` |
| `ENABLE_TRACING` | Enable OpenTelemetry tracing | `true` |

---

# MCP Configuration

| Variable | Description | Default |
|-----------|-------------|---------|
| `MCP_TIMEOUT` | Timeout (seconds) for MCP requests | `30` |
| `MCP_MAX_CONNECTIONS` | Maximum concurrent MCP connections | `20` |

---

# Plugin Configuration

| Variable | Description | Default |
|-----------|-------------|---------|
| `PLUGIN_AUTO_DISCOVERY` | Automatically discover plugins | `true` |
| `PLUGIN_DIRECTORY` | Plugin directory | `plugins` |

---

# Performance Configuration

| Variable | Description | Default |
|-----------|-------------|---------|
| `MAX_CONCURRENT_REQUESTS` | Maximum simultaneous requests | `100` |
| `REQUEST_TIMEOUT` | API timeout (seconds) | `60` |

---

# Frontend Configuration

The frontend can use its own `.env.local` file.

Example:

```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

| Variable | Description |
|-----------|-------------|
| `NEXT_PUBLIC_API_URL` | Backend API endpoint |

---

# Docker Configuration

Docker Compose automatically loads environment variables from the configured `.env` files.

Example:

```yaml
services:
  ai-gateway:
    env_file:
      - ai-gateway/.env
```

---

# Production Recommendations

For production deployments:

- Disable debug mode.
- Use HTTPS.
- Store secrets in a secure secret manager.
- Rotate API keys regularly.
- Restrict CORS to trusted origins.
- Enable monitoring and tracing.
- Run containers as a non-root user.
- Configure resource limits.

---

# Secrets Management

Never commit secrets to the repository.

Recommended secret management solutions include:

- AWS Secrets Manager
- Azure Key Vault
- HashiCorp Vault
- Docker Secrets
- Kubernetes Secrets

---

# Configuration Validation

The application validates configuration during startup.

Common validation checks include:

- Required environment variables are present.
- Port numbers are valid.
- Timeout values are positive.
- Logging levels are supported.
- API keys are provided when required.

If validation fails, the application exits with a descriptive error message.

---

# Example Development Configuration

```env
OPENAI_API_KEY=your_api_key
OPENAI_MODEL=gpt-4.1-mini

HOST=0.0.0.0
PORT=8000
DEBUG=true

LOG_LEVEL=DEBUG

ENABLE_METRICS=true
ENABLE_TRACING=true

MCP_TIMEOUT=30
MCP_MAX_CONNECTIONS=20

PLUGIN_AUTO_DISCOVERY=true
PLUGIN_DIRECTORY=plugins

MAX_CONCURRENT_REQUESTS=100
REQUEST_TIMEOUT=60
```

---

# Configuration Best Practices

- Keep secrets out of version control.
- Use separate configuration for development, staging, and production.
- Document new environment variables as they are introduced.
- Use descriptive names for configuration values.
- Validate configuration during application startup.
- Prefer environment variables over hardcoded values.

---
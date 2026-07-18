# Project Structure

This document provides an overview of the Enterprise MCP Platform repository and explains the purpose of each directory.

---

# Repository Overview

```text
enterprise-mcp-platform/

├── ai-gateway/
├── frontend/
├── infrastructure/
├── mcp-servers/
├── monitoring/
├── docs/
├── tests/
├── shared/
├── scripts/
├── docker-compose.yml
├── Makefile
└── README.md
```

---

# Root Directory

## `README.md`

The main entry point for the project.

Contains:

- Project overview
- Features
- Architecture
- Installation
- Quick Start
- Documentation links

---

## `docker-compose.yml`

Defines the local development environment.

Starts:

- AI Gateway
- Frontend
- Prometheus
- Grafana
- Supporting services

---

## `Makefile`

Provides common development commands such as:

- Build
- Run
- Test
- Lint
- Format

---

# AI Gateway

```text
ai-gateway/
```

The FastAPI backend and the core orchestration service.

Responsibilities:

- REST API
- Request validation
- AI orchestration
- Tool execution
- MCP communication
- Governance
- Plugin management
- Monitoring
- Memory
- Planning

---

## app/

Contains the application source code.

### api/

REST API endpoints.

Examples:

- Chat
- Health
- MCP
- Tools
- Servers

---

### approval/

Human approval and policy enforcement.

Includes:

- Approval requests
- Approval policies
- Audit trail
- Manual overrides

---

### core/

Application configuration.

Includes:

- Environment configuration
- Global settings

---

### db/

Database configuration and connection management.

---

### governance/

Enterprise governance components.

Includes:

- RBAC
- Policy engine
- Compliance
- Rate limiting
- Secret access
- Tool permissions

---

### hybrid_search/

Hybrid search implementation.

Includes:

- BM25
- Keyword search
- Metadata filtering
- Ranking fusion
- Vector abstraction

---

### memory/

Conversation and context memory.

Includes:

- Conversation history
- Session memory
- Long-term memory
- Semantic memory
- Memory ranking

---

### observability/

Application monitoring.

Includes:

- Metrics
- Logging
- OpenTelemetry
- Prometheus
- Grafana

---

### parallel/

Parallel task execution.

Includes:

- Worker pool
- Async queue
- Scheduler
- Cancellation
- Concurrency limits

---

### planner/

Execution planning engine.

Responsibilities:

- Dependency planning
- Retry management
- Cost optimization
- Timeout management
- Execution graphs

---

### plugins/

Plugin architecture.

Responsibilities:

- Plugin loading
- Registry
- Version management
- Sandboxing

---

### reasoning/

Reasoning components.

Responsibilities:

- Decision making
- Goal tracking
- Reflection
- Self critique
- Tool planning

---

### schemas/

Pydantic request and response models.

---

### services/

Business logic.

Contains:

- AI services
- Conversation services
- Planning services
- Tool routing
- Context management
- Execution services

---

### tool_selection/

Tool selection engine.

Responsibilities:

- Capability matching
- Intent classification
- Confidence scoring
- Tool ranking
- Fallback handling

---

### tests/

Backend unit tests.

Organized by module.

---

# Frontend

```text
frontend/
```

Modern web interface built with Next.js.

Responsibilities:

- Chat interface
- Dashboard
- Monitoring
- Server management
- Settings
- Activity history

---

## app/

Next.js App Router pages.

---

## components/

Reusable React components.

Examples:

- Chat
- Dashboard
- Sidebar
- Header
- Activity
- UI components

---

## services/

API client layer.

Responsible for communicating with the backend.

---

## store/

Application state management.

---

## types/

Shared TypeScript types.

---

## public/

Static assets.

---

# MCP Servers

```text
mcp-servers/
```

Independent MCP server implementations.

Current integrations include:

- AWS
- Docker
- GitHub
- Grafana
- Kubernetes
- PostgreSQL
- Prometheus

Each server exposes tools using the Model Context Protocol.

---

# Monitoring

```text
monitoring/
```

Monitoring infrastructure.

Contains:

- Prometheus configuration
- Grafana provisioning
- Alertmanager configuration
- Loki configuration

---

# Infrastructure

```text
infrastructure/
```

Deployment resources.

Includes:

## docker/

Docker-related files.

## kubernetes/

Kubernetes manifests.

## terraform/

Infrastructure as Code.

---

# Shared

```text
shared/
```

Reusable models and utilities shared across services.

---

# Scripts

```text
scripts/
```

Development and automation scripts.

Examples:

- Local setup
- Maintenance
- Utility scripts

---

# Tests

```text
tests/
```

Project-wide test suites.

Includes:

- Unit tests
- Integration tests
- Functional tests

---

# Documentation

```text
docs/
```

Project documentation.

Includes:

- Architecture
- Installation
- Configuration
- API reference
- Deployment
- Monitoring
- Testing

---

# Design Principles

The repository follows these principles:

- Modular architecture
- Clear separation of concerns
- Independent components
- Reusable services
- Enterprise scalability
- Container-first development
- Test-driven development
- Maintainable code organization

---

# Development Workflow

Typical workflow:

```text
Clone Repository
        │
        ▼
Install Dependencies
        │
        ▼
Configure Environment
        │
        ▼
Run Docker Compose
        │
        ▼
Start Frontend
        │
        ▼
Run Tests
        │
        ▼
Develop New Features
```

---

# Where to Add New Code

| Component | Directory |
|-----------|-----------|
| API Endpoints | `ai-gateway/app/api/` |
| Business Logic | `ai-gateway/app/services/` |
| Plugins | `ai-gateway/app/plugins/` |
| MCP Servers | `mcp-servers/` |
| Frontend Pages | `frontend/app/` |
| React Components | `frontend/components/` |
| Monitoring | `monitoring/` |
| Infrastructure | `infrastructure/` |
| Tests | `tests/` |
| Documentation | `docs/` |
# Testing Guide

This document describes the testing strategy, tools, and best practices used by the **Enterprise MCP Platform**.

---

# Overview

Testing helps ensure the platform remains reliable, secure, and maintainable as it evolves.

The project includes automated tests for:

- Backend APIs
- Business logic
- MCP integration
- Plugin system
- Frontend components
- End-to-end workflows

Testing should be part of every development cycle and run before submitting changes.

---

# Testing Philosophy

The project follows these principles:

- Write tests for new functionality.
- Keep tests independent and repeatable.
- Prefer automated over manual testing.
- Test behavior rather than implementation details.
- Fix failing tests before merging changes.

---

# Testing Stack

## Backend

| Tool | Purpose |
|------|---------|
| Pytest | Test framework |
| pytest-asyncio | Async endpoint testing |
| FastAPI TestClient | API testing |
| unittest.mock | Mocking dependencies |
| coverage.py | Code coverage |

---

## Frontend

| Tool | Purpose |
|------|---------|
| Jest | Unit testing |
| React Testing Library | Component testing |
| Playwright (recommended) | End-to-end testing |

---

# Test Directory Structure

```text
tests/

├── unit/
│   ├── api/
│   ├── services/
│   ├── planner/
│   ├── plugins/
│   ├── governance/
│   ├── memory/
│   ├── tool_selection/
│   └── observability/
│
├── integration/
│
├── e2e/
│
├── fixtures/
│
└── conftest.py
```

---

# Test Categories

## Unit Tests

Unit tests verify individual functions and classes in isolation.

Examples:

- Utility functions
- Planner logic
- Plugin loader
- Memory manager
- Policy validation

Unit tests should not depend on external services.

---

## Integration Tests

Integration tests verify interactions between multiple components.

Examples:

- API → Service layer
- Planner → MCP Core
- Plugin Manager → Registry
- Monitoring → Metrics endpoint

---

## API Tests

API tests verify REST endpoints.

Typical checks include:

- Status codes
- Request validation
- Response schema
- Error handling

Example:

```python
def test_health_endpoint(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"
```

---

## Plugin Tests

Plugin tests validate:

- Discovery
- Registration
- Initialization
- Execution
- Error handling
- Version compatibility

---

## MCP Tests

MCP-related tests verify:

- Server registration
- Session creation
- Tool discovery
- Tool execution
- Transport handling

External MCP servers should be mocked whenever possible.

---

## Frontend Tests

Frontend tests verify:

- Components render correctly
- User interactions
- Form validation
- API integration
- Error states

---

## End-to-End Tests

End-to-end tests simulate real user workflows.

Example scenarios:

- Open application
- Submit chat request
- Execute tool
- Display response
- Verify monitoring updates

---

# Running Tests

## Backend

Run all backend tests:

```bash
pytest
```

Run a specific directory:

```bash
pytest tests/unit
```

Run a specific file:

```bash
pytest tests/unit/test_plugins.py
```

Run a specific test:

```bash
pytest tests/unit/test_plugins.py::test_plugin_loading
```

---

## Frontend

Install dependencies:

```bash
npm install
```

Run tests:

```bash
npm test
```

---

## End-to-End

Run Playwright tests:

```bash
npx playwright test
```

---

# Code Coverage

Generate a coverage report:

```bash
coverage run -m pytest

coverage report

coverage html
```

Open the HTML report:

```text
htmlcov/index.html
```

Recommended coverage targets:

| Component | Target |
|-----------|--------|
| Backend | ≥ 90% |
| Frontend | ≥ 80% |
| Critical Modules | ≥ 95% |

Coverage is a guide—not a substitute for meaningful tests.

---

# Mocking

Mock external dependencies during tests, including:

- OpenAI API
- MCP servers
- External HTTP services
- Cloud services
- Databases

Example:

```python
from unittest.mock import patch

@patch("app.services.chat.OpenAIClient")
def test_chat(mock_client):
    ...
```

---

# Test Data

Use fixtures to create reusable test data.

Example:

```python
@pytest.fixture
def sample_request():
    return {
        "message": "Hello"
    }
```

Avoid hardcoding duplicate test data across multiple files.

---

# Continuous Integration

Tests should run automatically in CI for:

- Pull Requests
- Feature branches
- Main branch

Typical workflow:

1. Install dependencies
2. Run linting
3. Run unit tests
4. Run integration tests
5. Generate coverage
6. Build application

---

# Performance Testing

Recommended tools:

- Locust
- k6

Example metrics:

- Requests per second
- Response latency
- Concurrent users
- Error rate

---

# Security Testing

Regularly test:

- Input validation
- Authentication (when implemented)
- Authorization
- Rate limiting
- Secret handling
- Dependency vulnerabilities

Recommended tools:

- Trivy
- pip-audit
- npm audit
- GitHub CodeQL

---

# Best Practices

- Keep tests small and focused.
- Use descriptive test names.
- Avoid shared mutable state.
- Prefer fixtures over duplicated setup.
- Mock external services.
- Test edge cases and error paths.
- Ensure tests are deterministic.

---

# Troubleshooting

## Tests Fail Unexpectedly

Verify:

- Virtual environment is active.
- Dependencies are installed.
- Environment variables are configured.
- Services required for integration tests are running.

---

## Coverage Is Low

Review:

- Untested modules
- Missing edge-case tests
- New features without accompanying tests

---

## Flaky Tests

Check for:

- Timing issues
- Shared state
- Network dependencies
- Unmocked external services

---
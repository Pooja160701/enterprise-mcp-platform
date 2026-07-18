# Contributing to Enterprise MCP Platform

First of all, thank you for your interest in contributing to **Enterprise MCP Platform**! 🎉

Whether you're fixing a bug, improving documentation, adding a new feature, or suggesting an enhancement, your contributions are greatly appreciated.

---

# Code of Conduct

Please read our [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md) before contributing.

By participating in this project, you agree to follow its guidelines.

---

# Ways to Contribute

You can contribute in many ways, including:

- Reporting bugs
- Suggesting new features
- Improving documentation
- Fixing existing issues
- Writing tests
- Improving performance
- Enhancing UI/UX
- Adding MCP server integrations
- Improving monitoring and observability

---

# Development Setup

## 1. Fork the Repository

Click **Fork** on GitHub and clone your fork.

```bash
git clone https://github.com/<your-username>/enterprise-mcp-platform.git
```

---

## 2. Create a Feature Branch

```bash
git checkout -b feature/my-feature
```

Branch naming examples:

```text
feature/add-github-server
feature/improve-dashboard
feature/add-authentication
bugfix/fix-health-endpoint
docs/update-readme
```

---

## 3. Install Dependencies

### Backend

```bash
cd ai-gateway

pip install -r requirements.txt
```

### Frontend

```bash
cd frontend

npm install
```

---

## 4. Run the Project

Using Docker:

```bash
docker compose up
```

Or run services individually during development.

---

# Coding Standards

## Python

- Follow PEP 8
- Use type hints
- Keep functions focused and readable
- Prefer descriptive variable names
- Write docstrings for public classes and functions

Format code using:

```bash
black .
```

Sort imports:

```bash
isort .
```

Lint code:

```bash
ruff check .
```

---

## TypeScript

- Use strict typing
- Prefer functional React components
- Avoid `any` whenever possible
- Keep components small and reusable

---

# Testing

Every new feature should include appropriate tests.

Run all tests:

```bash
pytest
```

Frontend:

```bash
npm test
```

Ensure existing tests continue to pass before submitting a pull request.

---

# Commit Message Guidelines

Use clear, descriptive commit messages.

Examples:

```text
feat: add GitHub MCP server

fix: resolve plugin loading issue

docs: improve installation guide

refactor: simplify tool registry

test: add planner unit tests
```

---

# Pull Request Process

Before opening a Pull Request:

- Ensure the project builds successfully.
- Run all tests.
- Update documentation if needed.
- Keep pull requests focused on a single topic.
- Describe the purpose of your changes clearly.

Your Pull Request should include:

- Summary of changes
- Motivation
- Testing performed
- Screenshots (if UI changes)

---

# Reporting Bugs

When opening an issue, please include:

- Operating System
- Python version
- Node.js version
- Docker version (if applicable)
- Steps to reproduce
- Expected behavior
- Actual behavior
- Error logs or screenshots

---

# Feature Requests

When suggesting a feature, include:

- Problem statement
- Proposed solution
- Benefits
- Possible implementation approach (optional)

---

# Project Structure

Please follow the existing project organization.

- Backend code → `ai-gateway/`
- Frontend code → `frontend/`
- MCP servers → `mcp-servers/`
- Monitoring → `monitoring/`
- Infrastructure → `infrastructure/`
- Documentation → `docs/`
- Tests → `tests/`

---

# Documentation

If your contribution changes functionality, please update the relevant documentation.

Examples include:

- README.md
- API documentation
- Architecture documentation
- Installation guide
- Deployment guide

---

# Security

Please **do not open public GitHub issues for security vulnerabilities**.

Instead, follow the instructions in [SECURITY.md](SECURITY.md).

---

# License

By contributing to this project, you agree that your contributions will be licensed under the MIT License.

---

Thank you for helping improve Enterprise MCP Platform! 🚀
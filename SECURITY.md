# Security Policy

Thank you for helping keep **Enterprise MCP Platform** secure.

The security of this project and its users is important. If you discover a security vulnerability, please report it responsibly so it can be investigated and resolved.

---

# Supported Versions

The following versions currently receive security updates.

| Version | Supported |
|----------|-----------|
| 1.x.x | ✅ Yes |
| < 1.0.0 | ❌ No |

Only the latest stable release is actively maintained.

---

# Reporting a Vulnerability

Please **do not disclose security vulnerabilities publicly** by creating a GitHub Issue.

Instead, report them privately by contacting the project maintainer.

When reporting a vulnerability, please include:

- Description of the issue
- Steps to reproduce
- Potential impact
- Affected version
- Proof of concept (if available)
- Suggested mitigation (optional)

Reports will be acknowledged as soon as possible and investigated promptly.

---

# Responsible Disclosure

Please allow a reasonable amount of time for the issue to be investigated and fixed before publicly disclosing the vulnerability.

We appreciate responsible disclosure practices that help protect users of the project.

---

# Security Best Practices

When deploying Enterprise MCP Platform:

## Environment Variables

- Never commit `.env` files.
- Store API keys securely.
- Rotate credentials periodically.
- Use different credentials for development and production.

---

## Authentication

If authentication is enabled:

- Use strong passwords.
- Enable multi-factor authentication (MFA) where available.
- Follow the principle of least privilege.

---

## Secrets Management

Do not hardcode:

- API keys
- Database credentials
- Cloud credentials
- Access tokens
- Private certificates

Use secure secret management solutions such as:

- Docker Secrets
- Kubernetes Secrets
- AWS Secrets Manager
- Azure Key Vault
- HashiCorp Vault

---

## Dependencies

Regularly update project dependencies to receive the latest security fixes.

Recommended tools:

- Dependabot
- pip-audit
- npm audit
- Trivy
- GitHub Code Scanning

---

## Docker

For production deployments:

- Use minimal base images.
- Avoid running containers as the root user.
- Scan container images regularly.
- Keep images updated.

---

## API Security

The platform should be configured with:

- Input validation
- Authentication
- Authorization
- HTTPS
- CORS restrictions
- Rate limiting
- Request logging

---

## MCP Servers

Only connect to trusted MCP servers.

Review server permissions before enabling new integrations.

---

## OpenAI API Keys

Keep OpenAI API keys private.

Never:

- Commit keys to Git
- Share keys publicly
- Embed keys in frontend code

Always load secrets from environment variables.

---

# Security Updates

Security fixes will be included in future releases and documented in the project's CHANGELOG.

---

# Acknowledgements

We appreciate responsible security research and thank everyone who helps improve the security of Enterprise MCP Platform.
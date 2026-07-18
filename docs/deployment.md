# Deployment Guide

This document explains how to deploy the **Enterprise MCP Platform** in development and production environments.

---

# Overview

The platform supports multiple deployment strategies:

- Local Development
- Docker Compose
- Kubernetes
- Cloud Virtual Machines
- CI/CD Automation

The recommended production deployment uses:

- Docker
- Kubernetes
- GitHub Actions
- Terraform
- Prometheus
- Grafana

---

# Deployment Architecture

```
                    Internet
                        │
                        ▼
                Reverse Proxy / Load Balancer
                        │
                        ▼
              ┌───────────────────────┐
              │   Enterprise MCP App  │
              └──────────┬────────────┘
                         │
      ┌──────────────────┼──────────────────┐
      ▼                  ▼                  ▼
 AI Gateway         Frontend          Monitoring
      │                                     │
      ▼                                     ▼
 MCP Servers                        Prometheus
                                            │
                                            ▼
                                        Grafana
```

---

# Prerequisites

Before deployment, ensure the following are installed:

| Software | Recommended Version |
|----------|---------------------|
| Docker | Latest |
| Docker Compose | Latest |
| Kubernetes (Optional) | Latest |
| kubectl | Latest |
| Helm (Optional) | Latest |
| Terraform (Optional) | Latest |

---

# Environment Configuration

Create the required environment variables.

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

Never commit secrets to source control.

---

# Local Deployment

Start the backend:

```bash
cd ai-gateway

uvicorn app.main:app --reload
```

Start the frontend:

```bash
cd frontend

npm install

npm run dev
```

---

# Docker Deployment

Build images:

```bash
docker compose build
```

Start all services:

```bash
docker compose up -d
```

Check service status:

```bash
docker compose ps
```

Stop services:

```bash
docker compose down
```

---

# Kubernetes Deployment

Apply Kubernetes manifests:

```bash
kubectl apply -f infrastructure/kubernetes/
```

Verify deployments:

```bash
kubectl get pods

kubectl get services
```

Check logs:

```bash
kubectl logs <pod-name>
```

Delete resources:

```bash
kubectl delete -f infrastructure/kubernetes/
```

---

# Infrastructure as Code

Infrastructure can be provisioned using Terraform.

Example:

```bash
cd infrastructure/terraform

terraform init

terraform plan

terraform apply
```

Destroy infrastructure:

```bash
terraform destroy
```

---

# CI/CD Deployment

The project is designed to work with GitHub Actions.

Typical deployment workflow:

```
Push Code
     │
     ▼
GitHub Actions
     │
     ▼
Run Tests
     │
     ▼
Build Docker Images
     │
     ▼
Security Scans
     │
     ▼
Deploy
```

Recommended CI pipeline:

- Install dependencies
- Run linting
- Execute backend tests
- Execute frontend tests
- Generate coverage
- Build Docker images
- Scan dependencies
- Deploy production images

---

# Production Checklist

Before deploying:

- Production environment variables configured
- Debug mode disabled
- HTTPS enabled
- Secrets stored securely
- Monitoring enabled
- Health endpoint verified
- Backup strategy defined
- Dependencies updated
- Docker images scanned

---

# Health Verification

Verify backend:

```bash
curl http://localhost:8000/health
```

Expected response:

```json
{
  "status": "healthy"
}
```

Verify:

- Frontend loads successfully
- API documentation is accessible
- Monitoring dashboards are available
- MCP servers are connected

---

# Monitoring

Recommended production monitoring:

- Prometheus
- Grafana
- OpenTelemetry
- Structured Logging

Verify:

```
http://localhost:9090
```

```
http://localhost:3001
```

---

# Scaling

The platform can be scaled horizontally.

Recommendations:

- Multiple FastAPI instances
- Load balancer
- Horizontal Pod Autoscaler (Kubernetes)
- Resource limits
- Health probes

---

# Security Recommendations

Production deployments should:

- Use HTTPS
- Store secrets securely
- Restrict CORS origins
- Run containers as non-root
- Rotate API keys regularly
- Enable audit logging
- Keep dependencies updated

---

# Rollback Strategy

If a deployment fails:

1. Stop the deployment.
2. Roll back to the previous container image.
3. Verify application health.
4. Restore monitoring.
5. Investigate logs before redeploying.

Example:

```bash
kubectl rollout undo deployment/ai-gateway
```

---

# Troubleshooting

## Backend Does Not Start

Verify:

- Environment variables
- Python dependencies
- Docker logs
- Port availability

---

## Frontend Cannot Connect

Check:

- Backend URL
- CORS configuration
- Network connectivity
- Reverse proxy settings

---

## Kubernetes Pods Crash

Inspect pod status:

```bash
kubectl describe pod <pod-name>

kubectl logs <pod-name>
```

---

## Docker Containers Exit Immediately

Review logs:

```bash
docker compose logs
```

Check:

- Missing environment variables
- Incorrect volume mounts
- Configuration errors

---

# Future Improvements

Potential deployment enhancements include:

- Blue/Green deployments
- Canary deployments
- GitOps with Argo CD or Flux
- Automated rollback on health check failures
- Multi-region deployment
- Autoscaling based on custom metrics

---
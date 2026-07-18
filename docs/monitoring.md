# Monitoring Guide

This document describes the monitoring and observability capabilities of the **Enterprise MCP Platform**.

The platform includes built-in support for metrics, logging, tracing, and dashboards to help monitor application health, performance, and reliability.

---

# Overview

The monitoring stack provides visibility into:

- API performance
- MCP server health
- Tool execution
- System resource usage
- Application logs
- Request tracing
- Error rates

The default monitoring stack consists of:

- Prometheus
- Grafana
- OpenTelemetry
- Structured application logging

---

# Monitoring Architecture

```
                    Enterprise MCP Platform
                              │
        ┌─────────────────────┼─────────────────────┐
        ▼                     ▼                     ▼
   Application Logs      Prometheus Metrics    OpenTelemetry
        │                     │                     │
        ▼                     ▼                     ▼
   Log Storage          Prometheus Server      Trace Collector
                              │
                              ▼
                          Grafana
                              │
                              ▼
                      Dashboards & Alerts
```

---

# Components

## Prometheus

Prometheus collects time-series metrics from the platform.

Responsibilities:

- Metrics collection
- Metrics storage
- Service scraping
- Querying

Default endpoint:

```
http://localhost:9090
```

---

## Grafana

Grafana provides dashboards for visualizing metrics.

Typical dashboards include:

- API performance
- Request rate
- Error rate
- Tool execution
- MCP server status
- System health

Default URL:

```
http://localhost:3001
```

---

## OpenTelemetry

OpenTelemetry captures distributed traces across the platform.

Typical trace flow:

```
Frontend

↓

FastAPI

↓

Planner

↓

Plugin Manager

↓

MCP Server

↓

External Service
```

Traces help identify latency and failures across components.

---

## Structured Logging

Application logs are structured to simplify searching and analysis.

Log entries typically include:

- Timestamp
- Log level
- Request ID
- Component
- Message
- Execution duration

Example:

```json
{
  "timestamp": "2026-07-18T10:15:42Z",
  "level": "INFO",
  "component": "planner",
  "request_id": "req-12345",
  "message": "Tool execution completed",
  "duration_ms": 182
}
```

---

# Metrics

The platform exposes Prometheus-compatible metrics through:

```
GET /metrics
```

Example metric:

```
# HELP http_requests_total
# TYPE http_requests_total counter
http_requests_total 1542
```

---

# Core Metrics

## API Metrics

Collected metrics include:

- Request count
- Request duration
- Success rate
- Error rate
- Active requests

---

## MCP Metrics

Examples:

- Connected servers
- Active sessions
- Tool executions
- Discovery failures
- Execution failures

---

## Plugin Metrics

Examples:

- Loaded plugins
- Plugin execution count
- Plugin failures
- Plugin latency

---

## Planner Metrics

Examples:

- Planning duration
- Parallel tasks executed
- Retry count
- Timeout count

---

## Memory Metrics

Examples:

- Memory lookups
- Cache hits
- Cache misses
- Context size

---

# Dashboard Overview

Recommended Grafana dashboards include:

## Platform Overview

Displays:

- Platform status
- Request throughput
- Error rate
- Active sessions

---

## API Dashboard

Displays:

- Requests per second
- Latency
- HTTP status codes
- Response time percentiles

---

## MCP Dashboard

Displays:

- Connected servers
- Tool execution rate
- Discovery status
- Server health

---

## Plugin Dashboard

Displays:

- Active plugins
- Plugin failures
- Plugin execution latency

---

## System Dashboard

Displays:

- CPU usage
- Memory usage
- Disk utilization
- Network traffic

---

# Alerts

Recommended alerts include:

| Alert | Description |
|--------|-------------|
| High Error Rate | API errors exceed threshold |
| High Latency | Response times exceed target |
| MCP Server Offline | A registered server becomes unavailable |
| Plugin Failure | Plugin initialization or execution fails |
| High CPU Usage | CPU exceeds configured threshold |
| Low Available Memory | Memory usage exceeds threshold |

Alerts can be configured in Grafana or Prometheus Alertmanager.

---

# Health Checks

The platform exposes a health endpoint.

```
GET /health
```

Example response:

```json
{
  "status": "healthy"
}
```

Health checks verify:

- API availability
- MCP connectivity
- Plugin initialization
- Configuration validity

---

# Running the Monitoring Stack

Start all services:

```bash
docker compose up
```

Verify:

Prometheus:

```
http://localhost:9090
```

Grafana:

```
http://localhost:3001
```

Backend:

```
http://localhost:8000
```

Metrics:

```
http://localhost:8000/metrics
```

---

# Configuration

Monitoring behavior is configured using environment variables.

Example:

```env
ENABLE_METRICS=true

ENABLE_TRACING=true

LOG_LEVEL=INFO
```

Refer to `docs/configuration.md` for the complete configuration reference.

---

# Best Practices

- Monitor API latency continuously.
- Collect only useful metrics to reduce overhead.
- Use structured logging.
- Correlate logs and traces with request IDs.
- Configure meaningful alert thresholds.
- Rotate and retain logs according to operational requirements.
- Regularly review dashboards and alerts.

---

# Troubleshooting

## Metrics Not Appearing

Verify:

- Metrics are enabled.
- `/metrics` is accessible.
- Prometheus scrape configuration is correct.

---

## Grafana Dashboard Empty

Check:

- Prometheus is running.
- Prometheus is configured as a Grafana data source.
- Metrics are being collected.

---

## Missing Traces

Verify:

- Tracing is enabled.
- OpenTelemetry configuration is correct.
- Trace collector is reachable.

---

## High API Latency

Review:

- Request traces
- Backend logs
- MCP server responsiveness
- Resource utilization

---

# Future Enhancements

Planned improvements include:

- Loki integration for centralized log aggregation
- Alertmanager notification channels
- Custom Grafana dashboards
- Distributed metrics aggregation
- Service-level objectives (SLOs)
- Service-level indicators (SLIs)

---
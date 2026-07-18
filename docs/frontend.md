# Frontend Guide

This document describes the frontend architecture, development workflow, and best practices for the **Enterprise MCP Platform**.

---

# Overview

The frontend is built with **Next.js**, **React**, and **TypeScript**, providing a modern, responsive interface for interacting with the Enterprise MCP Platform.

The frontend communicates with the FastAPI backend through REST APIs and displays:

- AI Chat Interface
- Dashboard
- MCP Server Management
- Tool Explorer
- Activity Timeline
- Monitoring Dashboard
- Settings

---

# Technology Stack

| Technology | Purpose |
|------------|---------|
| Next.js | React Framework |
| React | UI Library |
| TypeScript | Static Typing |
| Tailwind CSS | Styling |
| React Hooks | State Management |
| Fetch API | Backend Communication |

---

# Directory Structure

```text
frontend/

├── app/
├── components/
├── hooks/
├── lib/
├── services/
├── store/
├── styles/
├── public/
├── types/
├── package.json
└── next.config.ts
```

---

# Application Structure

## app/

Contains all Next.js pages and layouts.

Example:

```text
app/

├── layout.tsx
├── page.tsx
├── chat/
├── dashboard/
├── monitoring/
├── settings/
└── servers/
```

Responsibilities:

- Routing
- Layouts
- Page composition

---

## components/

Reusable UI components.

Example:

```text
components/

├── chat/
├── dashboard/
├── layout/
├── monitoring/
├── servers/
├── ui/
└── common/
```

Typical components include:

- Sidebar
- Header
- Chat Window
- Message Bubble
- Dashboard Cards
- Tool Cards
- Server Status
- Activity Timeline
- Loading Spinner
- Modal Dialog
- Toast Notifications

---

## hooks/

Reusable custom React hooks.

Examples:

- useChat()
- useApi()
- useServerStatus()
- useTheme()

---

## lib/

Shared frontend utilities.

Examples:

- API helpers
- Constants
- Utility functions
- Formatters

---

## services/

Responsible for communicating with the backend.

Example:

```text
services/

api.ts
chat.ts
servers.ts
monitoring.ts
tools.ts
```

All HTTP requests should be centralized here.

---

## store/

Application state management.

Examples:

- Chat state
- User preferences
- Server status
- Dashboard state

---

## styles/

Global styling resources.

Contains:

- Global CSS
- Tailwind configuration
- Shared styles

---

## public/

Static assets.

Examples:

- Images
- Icons
- Logos
- Favicon

---

## types/

Shared TypeScript interfaces.

Examples:

```typescript
ChatMessage

Tool

Server

ApiResponse

DashboardStats
```

---

# Page Overview

## Dashboard

Displays:

- Platform overview
- Active MCP servers
- Running tools
- Request statistics
- System health

---

## Chat

Provides conversational interaction with the AI Gateway.

Features:

- Streaming responses
- Conversation history
- Markdown rendering
- Code blocks
- Tool execution feedback

---

## Servers

Displays:

- Registered MCP servers
- Server health
- Available tools
- Connection status

---

## Monitoring

Displays:

- API latency
- Error rate
- Tool execution metrics
- Active sessions
- Resource usage

---

## Settings

Allows configuration of:

- API endpoint
- Theme
- User preferences
- Application settings

---

# API Communication

The frontend communicates with the backend using REST APIs.

Example:

```
Frontend
     │
     ▼
services/chat.ts
     │
     ▼
Fetch API
     │
     ▼
FastAPI Backend
```

Example request:

```typescript
const response = await fetch("/api/chat", {
  method: "POST",
  headers: {
    "Content-Type": "application/json"
  },
  body: JSON.stringify(payload)
});
```

---

# State Management

State is organized by feature.

Examples:

- Chat
- Dashboard
- Monitoring
- Servers
- Settings

State should remain local whenever possible and be shared only when necessary.

---

# Styling

The project uses **Tailwind CSS**.

Guidelines:

- Prefer utility classes.
- Reuse shared UI components.
- Avoid inline styles.
- Keep layouts responsive.
- Support both light and dark themes where applicable.

---

# Error Handling

Frontend errors should provide clear feedback to users.

Examples:

- Network failures
- API validation errors
- Server unavailable
- Request timeout

Display:

- Toast notifications
- Error banners
- Retry actions

---

# Development Workflow

Install dependencies:

```bash
npm install
```

Run the development server:

```bash
npm run dev
```

Production build:

```bash
npm run build
```

Preview the production build:

```bash
npm start
```

---

# Testing

Recommended testing strategy:

- Unit tests for components
- Integration tests for pages
- API mocking
- End-to-end testing

Run tests:

```bash
npm test
```

---

# Performance Best Practices

- Lazy load large components.
- Optimize images using Next.js Image.
- Minimize unnecessary re-renders.
- Cache API responses where appropriate.
- Keep component trees shallow.
- Split code using dynamic imports.

---

# Accessibility

The frontend aims to follow accessibility best practices.

Recommendations:

- Use semantic HTML.
- Ensure keyboard navigation.
- Provide descriptive labels.
- Maintain sufficient color contrast.
- Add alternative text for images.

---

# Troubleshooting

## Frontend fails to start

```bash
rm -rf node_modules
rm package-lock.json

npm install
```

On Windows:

```powershell
rmdir /s /q node_modules
del package-lock.json

npm install
```

---

## Backend connection issues

Verify:

- Backend is running.
- `NEXT_PUBLIC_API_URL` is correctly configured.
- CORS settings allow frontend requests.

---

## Build errors

Run:

```bash
npm run build
```

Review TypeScript and ESLint errors before deploying.

---
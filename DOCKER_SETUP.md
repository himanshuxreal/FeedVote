# Docker Setup Guide for FeedVote

**Last Updated:** April 2026

This guide explains how to run FeedVote locally with Docker Compose.

---

## Prerequisites

1. Install Docker Desktop for Windows
   - Download: https://www.docker.com/products/docker-desktop
   - Restart your terminal after installation

2. Verify installation

```powershell
docker --version
docker-compose --version
```

---

## Quick Start

```powershell
docker-compose build
docker-compose up -d
```

Open the app in your browser:

- Frontend: http://localhost:8501
- Backend API docs: http://localhost:8000/docs

Stop services:

```powershell
docker-compose down
```

---

## Docker Development

This project currently supports local Docker development using `docker-compose.yml`.

### Start services

```powershell
docker-compose build
docker-compose up -d
```

### Confirm access

- Frontend: http://localhost:8501
- Backend: http://localhost:8000
- API docs: http://localhost:8000/docs

---

## Environment Variables

Use `.env.example` as a template to create `.env` if needed.

Example development values:

```text
DATABASE_URL=sqlite:///./feedvote.db
BACKEND_URL=http://backend:8000
```

---

## Common Commands

| Task | Command |
|------|---------|
| Build images | `docker-compose build` |
| Start containers | `docker-compose up -d` |
| View logs | `docker-compose logs -f` |
| Stop services | `docker-compose down` |
| Rebuild without cache | `docker-compose build --no-cache` |
| Show containers | `docker-compose ps` |

---

## Data Persistence

The backend uses SQLite for local development.

- Database file: `backend/feedvote.db`
- Survives container restarts while the file remains on disk
- To reset, stop services and remove `backend/feedvote.db`

```powershell
docker-compose down
Remove-Item backend\feedvote.db
docker-compose up -d
```

---

## Troubleshooting

### Docker command not found

Install Docker Desktop, restart your terminal, and run `docker --version`.

---

### Port conflict

```powershell
netstat -ano | findstr :8000
netstat -ano | findstr :8501
taskkill /PID <PID> /F
```

---

### Backend or frontend fails

```powershell
docker-compose logs -f backend
docker-compose logs -f frontend
```

If needed:

```powershell
docker-compose down -v
docker-compose build --no-cache
docker-compose up -d
```

---

## Notes

- This repository does not include a production `docker-compose` manifest.
- The current Docker setup is intended for local development.

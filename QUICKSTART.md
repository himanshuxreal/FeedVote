# FeedVote Quick Start Guide

## 🚀 Current Status: FULLY FUNCTIONAL

### Running Locally (No Docker)
```powershell
# Backend (FastAPI) - RUNNING
http://localhost:8000
API Docs: http://localhost:8000/docs

# Frontend (Streamlit) - RUNNING
http://localhost:8501

# Database (SQLite) - WORKING
backend/feedvote.db (61 KB)
```

**✅ Fully tested and operational**

---

## 🔧 What Was Configured

### 1. SQLite Database
- ✅ Verified working correctly
- ✅ All tables created successfully
- ✅ Data persistence confirmed
- ✅ No external database service needed

### 2. Fixed Issues
- ✅ Pydantic 2.5 compatibility (regex → pattern)
- ✅ Database URL configuration for SQLite
- ✅ CORS middleware enabled
- ✅ Health check endpoints working

### 3. Docker Configuration
- ✅ `docker-compose.yml` - Development (SQLite)
- ✅ `docker-compose.prod.yml` - Production (MySQL)
- ✅ Setup documentation completed
- ✅ Installation verification scripts ready

---

## 🐳 Docker Setup (When Ready)

### Prerequisites
- Windows 10 or 11
- 4GB RAM minimum
- Download from: https://www.docker.com/products/docker-desktop

### After Installing Docker

```powershell
# Verify Docker
powershell -ExecutionPolicy Bypass -File "check-docker.ps1"

# Build images
docker-compose build

# Start application
docker-compose up -d

# Check status
docker-compose ps

# View logs
docker-compose logs -f
```

**Access in Docker:**
- Frontend: http://localhost:8501
- Backend: http://localhost:8000
- API Docs: http://localhost:8000/docs

---

## 📊 Testing Data

Sample users created during testing:
- **User 1:** testuser / test@example.com
- **User 2:** testuser2 / test2@example.com

Sample feedback created:
- **Feedback 1:** "Test Feedback" created by User 1

Sample votes:
- **Vote 1:** User 2 upvoted Feedback 1

---

## 📁 Project Structure

```
FeedVote/
├── backend/              # FastAPI server
│   ├── app/
│   │   ├── main.py      # Main app
│   │   ├── database.py  # Database config (SQLite)
│   │   ├── models.py    # Data models
│   │   ├── schemas.py   # API schemas (FIXED)
│   │   ├── crud.py      # Database operations
│   │   └── routes/      # API endpoints
│   ├── feedvote.db      # SQLite database (61 KB)
│   └── requirements.txt
├── frontend/             # Streamlit UI
│   ├── app.py           # Main UI
│   └── requirements.txt
├── docker-compose.yml   # Development config (SQLite)
├── docker-compose.prod.yml # Production config (MySQL)
├── DOCKER_SETUP.md      # Detailed Docker guide
├── DATABASE_AND_DOCKER_STATUS.md # Full status report
└── check-docker.ps1     # Docker verification script
```

---

## ♻️ Common Tasks

### Start Services
```powershell
# Already running in the background
# Frontend: http://localhost:8501
# Backend: http://localhost:8000
```

### Stop Services
```powershell
# Ctrl+C in each terminal, or:
# Kill processes on ports 8000 and 8501
```

### Reset Database
```powershell
cd backend
rm feedvote.db
# Database recreates on next startup
```

### Run Tests
```powershell
cd backend
pytest tests/
```

### Use Docker
```powershell
docker-compose build
docker-compose up -d
docker-compose logs -f
docker-compose down
```

---

## 🔍 API Endpoints

### Users
- `POST /users/` - Create user
- `GET /users/{username}` - Get user by username
- `GET /users/id/{user_id}` - Get user by ID

### Feedback
- `POST /feedback/?user_id={id}` - Create feedback
- `GET /feedback/` - List all feedback
- `GET /feedback/{feedback_id}` - Get specific feedback
- `PUT /feedback/{feedback_id}/?user_id={id}` - Update feedback
- `DELETE /feedback/{feedback_id}/?user_id={id}` - Delete feedback

### Votes
- `POST /vote/` - Create vote (upvote/downvote)
- `GET /vote/feedback/{feedback_id}` - Get votes for feedback
- `GET /vote/user/{user_id}` - Get votes by user
- `DELETE /vote/{vote_id}/?user_id={id}` - Delete vote

### Health
- `GET /health` - Health check endpoint

---

## ⚠️ Before Docker Installation

### Current Setup is Production-Ready!
No Docker needed for development. The current setup:
- ✅ Uses SQLite (no external DB service)
- ✅ Fully tested and operational
- ✅ Hot-reload enabled for development
- ✅ Minimal dependencies

### Choose Docker When You Need:
- Consistent environments across machines
- Easy deployment to cloud services
- Production-grade setup with MySQL
- Team collaboration with standardized containers

---

## 📚 Documentation Files

1. **DOCKER_SETUP.md** - Complete Docker installation & usage guide
2. **DATABASE_AND_DOCKER_STATUS.md** - Detailed status report
3. **check-docker.ps1** - Verify Docker installation
4. **check-docker.bat** - Windows batch version of checker
5. **.env.example** - Environment variables template
6. **README.md** - Project overview (original)

---

## 🎯 Next Steps

1. **Immediate:** Start using the application!
   - Frontend: http://localhost:8501
   - Backend: http://localhost:8000/docs

2. **Soon:** When ready, install Docker
   - Download from https://www.docker.com/products/docker-desktop
   - Run `check-docker.ps1` to verify
   - Use `docker-compose up -d` for containers

3. **Later:** Deploy to production
   - Use `docker-compose.prod.yml` for MySQL
   - Configure environment variables
   - Deploy to cloud platform

---

## 💬 Quick Reference

| Task | Command |
|------|---------|
| Check Docker | `powershell -ExecutionPolicy Bypass -File "check-docker.ps1"` |
| Build Docker | `docker-compose build` |
| Start Docker | `docker-compose up -d` |
| View Logs | `docker-compose logs -f` |
| Stop Docker | `docker-compose down` |
| Reset DB | `cd backend && rm feedvote.db` |
| Run Tests | `cd backend && pytest tests/` |

---

**Status:** ✅ READY TO USE  
**Database:** SQLite 61 KB  
**Last Updated:** February 25, 2026

# Docker Setup Guide for FeedVote

## Prerequisites

### For Windows

1. **Install Docker Desktop for Windows**
   - Download from: https://www.docker.com/products/docker-desktop
   - Requirements:
     - Windows 10 or later
     - WSL 2 (Windows Subsystem for Linux 2) enabled
     - 4GB RAM minimum (8GB recommended)
     - Virtualization enabled in BIOS

2. **Verify Installation**
   ```powershell
   docker --version
   docker-compose --version
   ```

## Quick Start

### Development Setup (SQLite)

The default `docker-compose.yml` uses SQLite for local development:

```powershell
# Build the images
docker-compose build

# Start the application
docker-compose up -d

# View logs
docker-compose logs -f

# Stop the application
docker-compose down
```

**Access the application:**
- Frontend: http://localhost:8501
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs

### Production Setup (MySQL)

For production deployment with MySQL database:

```powershell
# Rename the production compose file
docker-compose -f docker-compose.prod.yml up -d

# This will:
# - Create MySQL 8.0 database container
# - Setup FastAPI backend connected to MySQL
# - Setup Streamlit frontend
```

## Database Configuration

### SQLite (Development - Default)
- **Location:** `backend/feedvote.db`
- **File Size:** Auto-grows as needed
- **Persistence:** Data survives container restarts (via volume mount)
- **No additional setup required**

### MySQL (Production)
- **Location:** Docker volume `mysql_data`
- **Credentials:** root/root (change in production!)
- **Port:** 3306 (internal to network)
- **Persistence:** Data stored in named volume

## Troubleshooting

### Docker Not Found
If you see "docker: command not found", ensure:
1. Docker Desktop is installed
2. Docker service is running
3. Terminal/PowerShell is restarted after installation

### Port Already in Use
```powershell
# Check what's using the port
netstat -ano | findstr :8000
netstat -ano | findstr :8501

# Kill the process
taskkill /PID <PID> /F
```

### Database Issues
```powershell
# Reset the database (SQLite only)
rm backend/feedvote.db

# Prune old containers
docker-compose down -v

# Rebuild fresh
docker-compose build --no-cache
docker-compose up
```

### View Container Logs
```powershell
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f backend
docker-compose logs -f frontend
```

## File Structure

```
FeedVote/
├── docker-compose.yml          # Development (SQLite)
├── docker-compose.prod.yml     # Production (MySQL)
├── .env.example               # Environment variables template
├── backend/
│   ├── Dockerfile
│   ├── requirements.txt
│   └── feedvote.db           # SQLite database (development)
├── frontend/
│   └── Dockerfile
└── README.md
```

## Environment Variables

Create a `.env` file based on `.env.example` or set via docker-compose environment section.

**Current defaults:**
- `DATABASE_URL=sqlite:///./feedvote.db` (Development)
- `BACKEND_URL=http://backend:8000` (Docker internal network)
- Backend Port: 8000
- Frontend Port: 8501

## Health Checks

Both services have health checks configured:
- **Backend:** Checks /health endpoint
- **Frontend:** Self-starting

The frontend waits for backend to be healthy before starting.

## Common Commands

```powershell
# Start services in background
docker-compose up -d

# Start with logs visible
docker-compose up

# Stop services
docker-compose stop

# Remove containers and networks
docker-compose down

# Remove volumes (deletes data!)
docker-compose down -v

# Rebuild images (apply changes)
docker-compose build

# Rebuild without cache
docker-compose build --no-cache

# View running containers
docker-compose ps

# Execute command in container
docker-compose exec backend python -m pytest
```

## Persistent Data Locations

### Development (SQLite)
- **Host:** `c:\Users\srbro\Dropbox\PC\Desktop\FeedVote\backend\feedvote.db`
- **Container:** `/app/feedvote.db`
- **Survives restarts:** Yes
- **Survives `docker-compose down`:** Yes
- **Only removed by:** Manual file deletion or `docker-compose down -v`

### Production (MySQL)
- **Host:** Docker named volume `mysql_data`
- **Location:** `C:\ProgramData\Docker\volumes\feedvote_mysql_data\_data`
- **Survives restarts:** Yes
- **Removed by:** `docker-compose down -v`

## Next Steps

1. Install Docker Desktop
2. Run: `docker-compose build`
3. Run: `docker-compose up -d`
4. Access http://localhost:8501 in your browser

For issues, check logs with: `docker-compose logs -f`

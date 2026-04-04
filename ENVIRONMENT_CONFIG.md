# FeedVote Environment Configuration

## Development (.env or direct in docker-compose.yml)

These are **already set** in docker-compose.yml by default:

```bash
# Backend
ENVIRONMENT=development
DATABASE_URL=sqlite:////tmp/feedvote.db
BACKEND_URL=http://backend:8000

# Frontend  
BACKEND_URL=http://backend:8000
```

No action needed for development. Just run: `docker-compose up -d`

---

## Production (.env file for docker-compose.prod.yml)

Create `.env` file in project root:

```bash
# MySQL Database Configuration
MYSQL_ROOT_PASSWORD=your-secure-root-password-here
MYSQL_DATABASE=feedvote
MYSQL_USER=feedvote
MYSQL_PASSWORD=your-secure-db-password-here

# Backend Configuration
ENVIRONMENT=production
# DATABASE_URL is automatically generated from above vars

# Frontend Configuration
BACKEND_URL=https://api.yourdomain.com  # Or http://backend:8000 for internal
```

Then run:
```bash
docker-compose -f docker-compose.prod.yml up -d
```

---

## Testing (CI/CD Pipeline)

These are **automatic** in the CI/CD workflow:

- Backend: `DATABASE_URL="sqlite:///./test.db"` (in conftest.py)
- Frontend: `BACKEND_URL="http://localhost:8000"` (from docker-compose)

CI/CD handles all test configuration automatically.

---

## Important Notes

### SQLite (Development)
- Database stored in: `backend_data` volume → `/tmp/feedvote.db`
- **Not** synced to host (clean separation)
- Persists across container restarts
- Deleted with: `docker-compose down -v`

### MySQL (Production)
- Database stored in: `mysql_data` volume
- Persists across container restarts
- Credentials required for security
- Connection: `mysql+pymysql://user:pass@db:3306/database`

### Healthchecks
- Backend: Checks `/health` endpoint (responds to curl)
- Frontend: Checks `/tmp/frontend-ready` file + curl response

### StartupBehavior
- Backend starts first
- Frontend waits for backend: `depends_on: service_healthy`
- Both create readiness markers in `/tmp/`

---

## Security Best Practices

### 🔒 Production Credentials

**Never:**
```bash
# ❌ Don't hard-code in files
database.yml: MYSQL_PASSWORD=hardcoded123

# ❌ Don't commit .env file
git add .env  # WRONG

# ❌ Don't use default passwords
MYSQL_PASSWORD=root
```

**Do:**
```bash
# ✅ Use environment variables
export MYSQL_PASSWORD="$(openssl rand -base64 32)"
docker-compose -f docker-compose.prod.yml up -d

# ✅ Use .env and .gitignore it
echo ".env" >> .gitignore
# Set secure values: MYSQL_PASSWORD, MYSQL_ROOT_PASSWORD

# ✅ Use secrets management
# AWS Secrets Manager, HashiCorp Vault, etc.
```

---

## Quick Reference

### Start Services

**Development:**
```bash
docker-compose up -d
```

**Production:**
```bash
# Set secure credentials first
export MYSQL_ROOT_PASSWORD="secure-root-pwd"
export MYSQL_PASSWORD="secure-db-pwd"

docker-compose -f docker-compose.prod.yml up -d
```

### Check Status

```bash
# View all services
docker-compose ps

# View detailed health
docker inspect feedvote-backend | jq '.State.Health'
docker inspect feedvote-frontend | jq '.State.Health'

# View logs
docker-compose logs -f backend
docker-compose logs -f frontend
```

### Stop & Cleanup

```bash
# Stop services (keep volumes)
docker-compose stop

# Stop and remove (clean slate for next start)
docker-compose down -v

# Stop with production file
docker-compose -f docker-compose.prod.yml down -v
```

---

## Environment Variable Reference

| Variable | Development | Production | Required |
|----------|-------------|-----------|----------|
| `ENVIRONMENT` | `development` | `production` | Optional (defaults shown) |
| `DATABASE_URL` | `sqlite:////tmp/feedvote.db` | Auto-generated from MySQL vars | Auto-generated |
| `MYSQL_ROOT_PASSWORD` | N/A | Required | Yes (prod only) |
| `MYSQL_DATABASE` | N/A | `feedvote` | Optional (default shown) |
| `MYSQL_USER` | N/A | `feedvote` | Optional (default shown) |
| `MYSQL_PASSWORD` | N/A | Required | Yes (prod only) |
| `BACKEND_URL` | `http://backend:8000` | `http://backend:8000` | Auto-set in compose |

---


#!/bin/bash
# FeedVote System Verification Script
# Run after `docker-compose up -d` to verify all services are healthy

set -e

echo "=========================================="
echo "FeedVote System Verification"
echo "=========================================="
echo ""

# Color codes
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

FAILED=0
PASSED=0

# Helper functions
pass() {
    echo -e "${GREEN}✓${NC} $1"
    ((PASSED++))
}

fail() {
    echo -e "${RED}✗${NC} $1"
    ((FAILED++))
}

warn() {
    echo -e "${YELLOW}⚠${NC} $1"
}

echo "1. Checking Docker and Docker Compose..."
echo ""

# Check Docker
if command -v docker &> /dev/null; then
    pass "Docker installed: $(docker --version | cut -d' ' -f3)"
else
    fail "Docker not installed"
    exit 1
fi

# Check Docker Compose
if command -v docker-compose &> /dev/null; then
    pass "Docker Compose installed: $(docker-compose --version | cut -d' ' -f3)"
else
    fail "Docker Compose not installed"
    exit 1
fi

echo ""
echo "2. Checking Docker Compose Configuration..."
echo ""

# Validate compose file
if docker-compose config > /dev/null 2>&1; then
    pass "docker-compose.yml is valid"
else
    fail "docker-compose.yml validation failed"
    docker-compose config
    exit 1
fi

echo ""
echo "3. Checking Container Status..."
echo ""

# Check if containers are running
BACKEND_RUNNING=$(docker ps --filter "name=feedvote-backend" --format "{{.Names}}" 2>/dev/null | wc -l)
FRONTEND_RUNNING=$(docker ps --filter "name=feedvote-frontend" --format "{{.Names}}" 2>/dev/null | wc -l)

if [ "$BACKEND_RUNNING" -gt 0 ]; then
    pass "Backend container is running"
else
    fail "Backend container is not running"
    FAILED=$((FAILED + 1))
fi

if [ "$FRONTEND_RUNNING" -gt 0 ]; then
    pass "Frontend container is running"
else
    fail "Frontend container is not running"
    FAILED=$((FAILED + 1))
fi

echo ""
echo "4. Checking Container Health..."
echo ""

# Check backend health state (from Docker)
BACKEND_STATE=$(docker inspect feedvote-backend 2>/dev/null | jq -r '.[] | .State.Health.Status' 2>/dev/null || echo "unknown")
if [ "$BACKEND_STATE" = "healthy" ]; then
    pass "Backend container is healthy"
elif [ "$BACKEND_STATE" = "starting" ]; then
    warn "Backend container is still starting (check again in 5 seconds)"
else
    fail "Backend container health: $BACKEND_STATE"
    FAILED=$((FAILED + 1))
fi

FRONTEND_STATE=$(docker inspect feedvote-frontend 2>/dev/null | jq -r '.[] | .State.Health.Status' 2>/dev/null || echo "unknown")
if [ "$FRONTEND_STATE" = "healthy" ]; then
    pass "Frontend container is healthy"
elif [ "$FRONTEND_STATE" = "starting" ]; then
    warn "Frontend container is still starting (check again in 5 seconds)"
else
    fail "Frontend container health: $FRONTEND_STATE"
    FAILED=$((FAILED + 1))
fi

echo ""
echo "5. Checking Network Connectivity..."
echo ""

# Check backend health endpoint
if curl -sf http://localhost:8000/health > /dev/null 2>&1; then
    pass "Backend health endpoint responding"
    
    # Get backend status
    BACKEND_RESPONSE=$(curl -s http://localhost:8000/health | jq -r '.status // "unknown"' 2>/dev/null || echo "error")
    pass "  → Status: $BACKEND_RESPONSE"
else
    fail "Backend health endpoint not responding (http://localhost:8000/health)"
    FAILED=$((FAILED + 1))
fi

# Check frontend
if curl -sf http://localhost:8501 > /dev/null 2>&1; then
    pass "Frontend is responding"
else
    fail "Frontend not responding (http://localhost:8501)"
    FAILED=$((FAILED + 1))
fi

echo ""
echo "6. Checking Readiness Markers..."
echo ""

# Check backend readiness marker
if docker exec feedvote-backend test -f /tmp/backend-ready 2>/dev/null; then
    pass "Backend readiness marker exists (/tmp/backend-ready)"
else
    fail "Backend readiness marker missing"
    FAILED=$((FAILED + 1))
fi

# Check frontend readiness marker
if docker exec feedvote-frontend test -f /tmp/frontend-ready 2>/dev/null; then
    pass "Frontend readiness marker exists (/tmp/frontend-ready)"
else
    fail "Frontend readiness marker missing"
    FAILED=$((FAILED + 1))
fi

echo ""
echo "7. Checking Database..."
echo ""

# Check if backend can connect to database
if docker exec feedvote-backend python -c "from app.database import SessionLocal; db = SessionLocal(); db.execute('SELECT 1'); db.close()" 2>/dev/null; then
    pass "Backend database connection verified"
else
    fail "Backend database connection failed"
    FAILED=$((FAILED + 1))
fi

# Check database file location (dev only, not production)
if docker exec feedvote-backend test -f /tmp/feedvote.db 2>/dev/null; then
    pass "SQLite database file exists at /tmp/feedvote.db"
elif docker exec feedvote-backend python -c "import os; print(os.getenv('DATABASE_URL', ''))" 2>/dev/null | grep -q "mysql"; then
    pass "Using MySQL database (production mode)"
else
    warn "Database file not found (may be OK for MySQL)"
fi

echo ""
echo "8. Checking API Endpoints..."
echo ""

# Root endpoint
if curl -sf http://localhost:8000/ > /dev/null 2>&1; then
    pass "Backend root endpoint (/) working"
else
    fail "Backend root endpoint (/) not working"
    FAILED=$((FAILED + 1))
fi

# API docs
if curl -sf http://localhost:8000/docs > /dev/null 2>&1; then
    pass "Backend API documentation (/docs) working"
else
    fail "Backend API documentation (/docs) not working"
    FAILED=$((FAILED + 1))
fi

if curl -sf http://localhost:8000/redoc > /dev/null 2>&1; then
    pass "Backend ReDoc documentation (/redoc) working"
else
    fail "Backend ReDoc documentation (/redoc) not working"
    FAILED=$((FAILED + 1))
fi

echo ""
echo "=========================================="
echo "Verification Summary"
echo "=========================================="
echo -e "Tests Passed: ${GREEN}$PASSED${NC}"
echo -e "Tests Failed: ${RED}$FAILED${NC}"
echo ""

if [ $FAILED -eq 0 ]; then
    echo -e "${GREEN}✓ All checks passed! System is healthy.${NC}"
    echo ""
    echo "Access the application:"
    echo "  Backend API: http://localhost:8000"
    echo "  API Docs:    http://localhost:8000/docs"
    echo "  Frontend:    http://localhost:8501"
    exit 0
else
    echo -e "${RED}✗ $FAILED check(s) failed. Review errors above.${NC}"
    echo ""
    echo "Troubleshooting steps:"
    echo "1. Check container logs: docker-compose logs backend frontend"
    echo "2. Ensure services are fully started (may take 30-40 seconds)"
    echo "3. Verify Docker Desktop has sufficient resources"
    echo "4. Try: docker-compose down -v && docker-compose up -d"
    exit 1
fi

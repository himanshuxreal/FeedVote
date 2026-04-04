#!/bin/bash
# Backend startup and health verification
# Ensures database is initialized before starting the app

set -e

echo "🔍 Environment: $ENVIRONMENT"
echo "📊 Database URL: $DATABASE_URL"

# Database initialization
echo "🗄️  Initializing database..."
python -c "
from app.database import Base, engine
print('Creating tables...')
Base.metadata.create_all(bind=engine)
print('✓ Database tables created/verified')
"

# Brief health verification before starting
echo "🏥 Running pre-startup health checks..."
python -c "
from app.database import SessionLocal
try:
    db = SessionLocal()
    db.execute('SELECT 1')
    db.close()
    print('✓ Database connection verified')
except Exception as e:
    print(f'✗ Database connection failed: {e}')
    exit(1)
"

# Signal readiness
touch /tmp/backend-ready
echo "✓ Backend ready for startup"

# Start the application
echo "🚀 Starting FastAPI application..."
exec uvicorn app.main:app --host 0.0.0.0 --port 8000

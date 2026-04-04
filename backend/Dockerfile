# ===========================
# Backend Dockerfile
# FeedVote FastAPI Server
# ===========================
# Build stage: uses python:3.10-slim for smaller image (45MB vs 385MB)

FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Set environment variables
# PYTHONDONTWRITEBYTECODE: Don't create .pyc files
# PYTHONUNBUFFERED: Don't buffer stdout/stderr
# DATABASE_URL: Use temp directory for SQLite, override with MYSQL for prod
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    ENVIRONMENT=development \
    DATABASE_URL="sqlite:////tmp/feedvote.db"

# Create non-root user for security (don't run as root)
RUN useradd -m -u 1000 appuser && \
    mkdir -p /app /tmp && \
    chown -R appuser:appuser /app /tmp

# Install system dependencies (minimal set)
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first (better Docker layer caching)
COPY --chown=appuser:appuser requirements.txt .

# Install Python dependencies
RUN pip install --upgrade pip setuptools wheel && \
    pip install -r requirements.txt

# Copy application code
COPY --chown=appuser:appuser . .

# Copy and make startup script executable
COPY --chown=appuser:appuser startup.sh /app/startup.sh
RUN chmod +x /app/startup.sh

# Switch to non-root user
USER appuser

# Expose port
EXPOSE 8000

# Health check - check if backend is responding
HEALTHCHECK --interval=30s --timeout=10s --start-period=500s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Run startup script
CMD ["/app/startup.sh"]

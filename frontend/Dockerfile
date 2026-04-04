# ===========================
# Frontend Dockerfile
# FeedVote Streamlit UI
# ===========================

FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    BACKEND_URL="http://backend:8000"

# Create non-root user for security
RUN useradd -m -u 1000 appuser && \
    mkdir -p /app && \
    chown -R appuser:appuser /app

# Install system dependencies (minimal set)
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY --chown=appuser:appuser requirements.txt .

# Install Python dependencies
RUN pip install --upgrade pip setuptools wheel && \
    pip install -r requirements.txt

# Copy application code
COPY --chown=appuser:appuser . .

# Copy and make startup script executable
COPY --chown=appuser:appuser startup.sh /app/startup.sh
RUN chmod +x /app/startup.sh

# Create Streamlit config directory with proper permissions
RUN mkdir -p /home/appuser/.streamlit && \
    chown -R appuser:appuser /home/appuser/.streamlit

# Create Streamlit configuration
RUN echo "[server]\n\
headless = true\n\
port = 8501\n\
enableCORS = false\n\
enableXsrfProtection = true\n\
maxMessageSize = 100\n\
\n\
[logger]\n\
level = info\n\
\n\
[client]\n\
showErrorDetails = true\n\
" > /home/appuser/.streamlit/config.toml

# Switch to non-root user
USER appuser

# Expose port
EXPOSE 8501

# Health check - file-based check (Streamlit doesn't expose standard health endpoint)
# Check if Streamlit process is running and frontend is ready
HEALTHCHECK --interval=10s --timeout=5s --start-period=500s --retries=3 \
    CMD (test -f /tmp/frontend-ready && curl -sf http://localhost:8501/) || exit 1

# Run application via startup script
CMD ["/app/startup.sh"]

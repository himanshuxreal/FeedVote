#!/bin/bash
# Frontend startup script with health verification

set -e

BACKEND_URL="${BACKEND_URL:-http://backend:8000}"
MAX_RETRIES=30
RETRY_INTERVAL=1

echo "🔍 Environment: BACKEND_URL=$BACKEND_URL"

# Wait for backend to be ready
echo "⏳ Waiting for backend to be ready..."
for i in $(seq 1 $MAX_RETRIES); do
    if curl -sf "$BACKEND_URL/health" >/dev/null 2>&1; then
        echo "✓ Backend is ready!"
        break
    fi
    echo "  Attempt $i/$MAX_RETRIES: Backend not ready..."
    sleep $RETRY_INTERVAL
    if [ $i -eq $MAX_RETRIES ]; then
        echo "⚠️  Backend still not ready, proceeding anyway (may fail later)"
        break
    fi
done

# Start Streamlit in the background
echo "🚀 Starting Streamlit application..."
streamlit run app.py \
    --server.port=8501 \
    --server.address=0.0.0.0 \
    --server.headless=true \
    --logger.level=info &

STREAMLIT_PID=$!

# Wait for Streamlit to actually start responding
echo "⏳ Waiting for Streamlit to be responsive..."
for i in $(seq 1 $MAX_RETRIES); do
    if curl -sf http://localhost:8501/ >/dev/null 2>&1; then
        echo "✓ Streamlit is responsive!"
        mkdir -p /tmp
        touch /tmp/frontend-ready
        echo "✓ Frontend ready marker created"
        break
    fi
    echo "  Attempt $i/$MAX_RETRIES: Streamlit not responsive yet..."
    sleep $RETRY_INTERVAL
done

# Keep container running
wait $STREAMLIT_PID

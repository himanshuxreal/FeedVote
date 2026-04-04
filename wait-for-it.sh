#!/usr/bin/env bash
# wait-for-it.sh: Wait for a service to be ready
# Usage: wait-for-it.sh [host]:[port] [-- command args]

set -e

host="$1"
shift
cmd="$@"

# Default retries and timeout
retries=30
timeout=5

echo "🔄 Waiting for $host to be ready (${retries} retries, ${timeout}s timeout)..."

for i in $(seq 1 $retries); do
    if echo >/dev/tcp/$host 2>/dev/null; then
        echo "✓ $host is ready!"
        break
    fi
    echo "  Attempt $i/$retries: $host not ready yet..."
    sleep 1
done

if [ -n "$cmd" ]; then
    echo "🚀 Executing: $cmd"
    exec $cmd
fi

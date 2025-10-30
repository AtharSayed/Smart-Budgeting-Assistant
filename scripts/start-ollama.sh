#!/bin/bash
# scripts/start-ollama.sh

set -e

echo "Starting Ollama server..."
ollama serve &
SERVER_PID=$!

# Give server time to boot
sleep 5

echo "Waiting for Ollama API to be ready..."
for i in {1..30}; do
    if curl -s http://localhost:11434/api/tags > /dev/null 2>&1; then
        echo "Ollama API is up!"
        break
    fi
    echo "Attempt $i/30: Waiting for API..."
    sleep 3
done

# Pull model if not exists
if ! ollama list | grep -q "mistral"; then
    echo "Pulling mistral model (~4.1GB)..."
    ollama pull mistral
else
    echo "Mistral already installed"
fi

echo "Ollama is ready and serving!"
wait $SERVER_PID
#!/bin/sh
set -e

echo "Starting Ollama (CPU)..."
ollama serve &
PID=$!

sleep 30

echo "Waiting for /api/tags..."
while ! wget -q --spider http://localhost:11434/api/tags 2>/dev/null; do
    echo "Waiting... (10s)"
    sleep 10
done

echo "Ollama API IS LIVE!"

if ! ollama list | grep -q "mistral"; then
    echo "Pulling mistral..."
    ollama pull mistral
else
    echo "mistral ready"
fi

echo "Ollama is READY!"
wait $PID
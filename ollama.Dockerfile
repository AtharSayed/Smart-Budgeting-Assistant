# ollama.Dockerfile
FROM ollama/ollama

# INSTALL CURL FOR SCRIPT & HEALTHCHECK
RUN apt-get update && \
    apt-get install -y --no-install-recommends curl && \
    rm -rf /var/lib/apt/lists/*

COPY scripts/start-ollama.sh /usr/local/bin/start-ollama.sh
RUN chmod +x /usr/local/bin/start-ollama.sh

ENTRYPOINT ["/usr/local/bin/start-ollama.sh"]
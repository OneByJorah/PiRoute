# =============================================================================
# EdgeRouter (PiRouter Pro) — Production Dockerfile
# python:3.11-slim base
# Tag: jorahone/edgerouter:latest
# =============================================================================

FROM python:3.11-slim AS builder

WORKDIR /build

# Install build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --user --upgrade pip && \
    pip install --no-cache-dir --user gunicorn && \
    pip install --no-cache-dir --user -r requirements.txt

# ---- Runtime Stage ----
FROM python:3.11-slim

# Create non-root user
RUN groupadd -r edgerouter && useradd -r -g edgerouter -d /app -s /sbin/nologin edgerouter

# Install runtime dependencies (speedtest-cli needs network access, psutil needs libc)
RUN apt-get update && apt-get install -y --no-install-recommends \
    ca-certificates \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy installed packages from builder
COPY --from=builder /root/.local /usr/local
COPY --from=builder /root/.local/bin /usr/local/bin

# Create application and data directories
RUN mkdir -p /app /var/lib/pirouter

# Copy application code
COPY . /app
WORKDIR /app

# Ensure template directory exists
RUN mkdir -p /app/template

# Set ownership
RUN chown -R edgerouter:edgerouter /app /var/lib/pirouter

# Switch to non-root user
USER edgerouter

# Expose application port
EXPOSE 5000

# Healthcheck — verify the app responds
HEALTHCHECK --interval=30s --timeout=5s --start-period=15s --retries=3 \
    CMD python3 -c "import urllib.request; urllib.request.urlopen('http://localhost:5000/')" || exit 1

# Run with gunicorn (production WSGI server)
# The app uses a background thread for traffic collection, so we use a custom entrypoint
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "2", "--threads", "4", "--timeout", "120", "--access-logfile", "-", "--error-logfile", "-", "app:app"]

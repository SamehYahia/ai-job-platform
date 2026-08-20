# syntax=docker/dockerfile:1

# Build dependency wheels separately to keep the runtime image smaller.
FROM python:3.12-slim-bookworm AS builder

ENV PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /build

COPY requirements.txt .

RUN python -m pip wheel \
    --wheel-dir=/wheels \
    --requirement requirements.txt


# The runtime stage contains only the application and installed dependencies.
FROM python:3.12-slim-bookworm AS runtime

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

RUN groupadd --gid 10001 appgroup \
    && useradd \
        --uid 10001 \
        --gid appgroup \
        --no-log-init \
        --create-home \
        appuser

WORKDIR /app

COPY requirements.txt .
COPY --from=builder /wheels /wheels

RUN python -m pip install \
        --no-cache-dir \
        --no-index \
        --find-links=/wheels \
        --requirement requirements.txt \
    && rm -rf /wheels

COPY --chown=appuser:appgroup app ./app
COPY --chown=appuser:appgroup alembic ./alembic
COPY --chown=appuser:appgroup alembic.ini ./
COPY scripts/start.sh /usr/local/bin/start-app

RUN chmod +x /usr/local/bin/start-app

USER appuser

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=3s --start-period=10s --retries=3 \
    CMD ["python", "-c", "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8000/health/live', timeout=2)"]

ENTRYPOINT ["/usr/local/bin/start-app"]
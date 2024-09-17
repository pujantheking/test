# Builder Stage
FROM python:3.11-slim AS builder

# Copy project files
COPY ./alembic.ini ./poetry.lock ./pyproject.toml /code/
COPY ./src /code
COPY .env /code/.env

# Set working directory
WORKDIR /code

# Install Python dependencies using poetry
RUN --mount=type=cache,target=/root/.cache,sharing=shared \
    pip install --upgrade pip && \
    pip install poetry && \
    poetry export -f requirements.txt --output requirements.txt --without-hashes && \
    pip install -r requirements.txt && \
    pip uninstall -y poetry && \
    rm -rf requirements.txt

# Runner Stage
FROM python:3.11-slim AS runner

# Set environment variables
ENV PYTHONUNBUFFERED 1
ENV PYTHONPATH "/code/src:${PYTHONPATH}"

# Copy files from the builder stage
COPY --from=builder /code /code
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages

# Install curl for healthcheck
RUN apt-get update && \
    apt-get install -y --no-install-recommends curl && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Healthcheck
HEALTHCHECK --interval=10s --timeout=3s --start-period=10s --retries=3 CMD curl -f http://localhost:80/healthcheck || exit 1

RUN useradd -m -s /bin/bash app

RUN usermod -aG root app

USER app

# Set working directory
WORKDIR /code

# Entrypoint
ENTRYPOINT ["/bin/sh", "-c" , "python main.py migrate && python main.py run"]

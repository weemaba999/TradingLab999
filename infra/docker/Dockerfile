FROM python:3.12-slim

WORKDIR /app

# System dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY tradinglab/ ./tradinglab/

ENV PYTHONPATH=/app
ENV TZ=Europe/Brussels

HEALTHCHECK --interval=60s --timeout=10s \
    CMD python -c "import redis; redis.Redis().ping()" || exit 1

CMD ["python", "-m", "tradinglab.main"]

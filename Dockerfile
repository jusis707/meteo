# Dockerfile
FROM mcr.microsoft.com/playwright/python:v1.53.0-jammy

WORKDIR /app

RUN groupadd -r appgroup && useradd -r -g appgroup appuser

RUN mkdir -p /app/output && chown -R appuser:appgroup /app/output

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN chown -R appuser:appgroup /app

USER appuser

CMD ["python", "./scraper.py"]

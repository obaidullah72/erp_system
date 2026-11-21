FROM python:3.11-slim
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1 PIP_NO_CACHE_DIR=1
WORKDIR /app
COPY requirements.lock ./
RUN pip install --no-cache-dir -r requirements.lock && useradd --create-home --uid 10001 erp
COPY --chown=erp:erp app ./app
COPY --chown=erp:erp scripts ./scripts
COPY --chown=erp:erp migrations ./migrations
COPY --chown=erp:erp alembic.ini ./
USER erp
EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--no-access-log"]

# --- Build del frontend ---
FROM node:24-slim AS frontend
WORKDIR /src
COPY frontend/package*.json ./
RUN npm ci
COPY frontend/ ./
RUN npm run build

# --- Backend + SPA ---
FROM python:3.13-slim
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1 TZ=America/Bogota
WORKDIR /srv/backend
COPY backend/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY backend/ ./
COPY --from=frontend /src/dist /srv/frontend/dist
RUN useradd -u 1000 -m app && chown -R app /srv
USER app
EXPOSE 8765
# Un solo worker: SQLite + rate-limit en memoria.
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8765", "--workers", "1", "--proxy-headers", "--forwarded-allow-ips", "*"]

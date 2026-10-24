FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
RUN chmod +x scripts/docker-entrypoint.sh

ENV PYTHONPATH=/app/src
EXPOSE 8010

ENTRYPOINT ["scripts/docker-entrypoint.sh"]

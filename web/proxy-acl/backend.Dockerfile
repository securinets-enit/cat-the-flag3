FROM python:3.11-alpine

COPY backend.py /app/backend.py
WORKDIR /app
USER nobody:nobody
EXPOSE 8080
CMD ["python3", "/app/backend.py"]
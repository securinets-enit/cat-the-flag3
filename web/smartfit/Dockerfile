FROM python:3.11-slim

# Create unprivileged user
RUN useradd -m -s /bin/false smartfit

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application source code
COPY app/ /app/
COPY flag.txt /flag.txt

# Set permissions: application files read-only, flag read-only for app user
RUN chown -R root:root /app && \
    chmod -R 755 /app && \
    chown root:smartfit /flag.txt && \
    chmod 640 /flag.txt

# Switch to non-root user
USER smartfit

EXPOSE 5000

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "2", "app:app"]

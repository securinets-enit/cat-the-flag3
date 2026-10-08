FROM python:3.11-slim

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    openssl \
    && rm -rf /var/lib/apt/lists/*

# Install python dependencies
RUN pip install --no-cache-dir cryptography pyfiglet

# Create ctf user
RUN useradd -m -s /bin/bash ctf

WORKDIR /home/ctf

# Copy source code and flag
COPY src/ /home/ctf/
COPY deploy/flag.txt /home/ctf/flag.txt

# Ensure certs exist (generate if needed)
RUN python /home/ctf/gen_cert.py

# Secure permissions
RUN chown -R root:ctf /home/ctf && \
    chmod 750 /home/ctf && \
    chmod 755 /home/ctf/*.py && \
    chmod 644 /home/ctf/cert.pem /home/ctf/key.pem /home/ctf/flag.txt

USER ctf

ENV PORT=5000
ENV ROUNDS=100
EXPOSE 5000

CMD ["python", "-u", "/home/ctf/server.py"]

FROM python:3.12-slim

RUN apt-get update && apt-get install -y --no-install-recommends socat \
    && rm -rf /var/lib/apt/lists/*

RUN useradd -m -s /usr/sbin/nologin ctf

COPY src/server.py /app/server.py
COPY flag.txt /app/flag.txt

RUN chown -R root:root /app && chmod 555 /app && chmod 444 /app/*

USER ctf
WORKDIR /app
EXPOSE 1344

# One fresh game per connection, killed after 120 seconds
CMD ["socat", "-T120", "TCP-LISTEN:1344,reuseaddr,fork", "EXEC:timeout -s KILL 120 python3 -u /app/server.py,stderr"]

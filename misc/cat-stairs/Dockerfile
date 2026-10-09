FROM python:3.12-slim

RUN apt-get update && apt-get install -y --no-install-recommends socat \
    && rm -rf /var/lib/apt/lists/*

RUN useradd -m -s /usr/sbin/nologin ctf

COPY src/server.py /app/server.py
COPY flag.txt /app/flag.txt

RUN chown -R root:root /app && chmod 555 /app && chmod 444 /app/*

USER ctf
WORKDIR /app
EXPOSE 1340

ENV ROUNDS=40 ROUND_TIME=3

# One fresh game per connection, killed after 150 seconds
CMD ["socat", "-T150", "TCP-LISTEN:1340,reuseaddr,fork", "EXEC:timeout -s KILL 150 python3 -u /app/server.py,stderr"]

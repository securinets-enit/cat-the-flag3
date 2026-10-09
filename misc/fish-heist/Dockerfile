FROM python:3.12-slim

RUN apt-get update && apt-get install -y --no-install-recommends socat \
    && rm -rf /var/lib/apt/lists/*

RUN useradd -m -s /usr/sbin/nologin ctf

COPY src/server.py /app/server.py
COPY flag.txt /app/flag.txt

RUN chown -R root:root /app && chmod 555 /app && chmod 444 /app/*

USER ctf
WORKDIR /app
EXPOSE 1341

ENV GAMES=20 MISERE_FROM=16 MOVE_TIME=10

# One fresh game per connection, killed after 300 seconds
CMD ["socat", "-T300", "TCP-LISTEN:1341,reuseaddr,fork", "EXEC:timeout -s KILL 300 python3 -u /app/server.py,stderr"]

FROM python:3.12-slim

RUN apt-get update && apt-get install -y --no-install-recommends socat \
    && rm -rf /var/lib/apt/lists/*

RUN useradd -m -s /usr/sbin/nologin ctf

COPY src/server.py /app/server.py
COPY flag.txt /app/flag.txt

RUN chown -R root:root /app && chmod 555 /app && chmod 444 /app/*

USER ctf
WORKDIR /app
EXPOSE 1343

ENV ROUNDS=10 QUESTIONS=26 LIES=2 ROUND_TIME=30

# One fresh game per connection, killed after 360 seconds
CMD ["socat", "-T360", "TCP-LISTEN:1343,reuseaddr,fork", "EXEC:timeout -s KILL 360 python3 -u /app/server.py,stderr"]

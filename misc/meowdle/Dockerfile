FROM python:3.12-slim

RUN apt-get update && apt-get install -y --no-install-recommends socat \
    && rm -rf /var/lib/apt/lists/*

RUN useradd -m -s /usr/sbin/nologin ctf

COPY src/server.py /app/server.py
COPY dist/words.txt /app/words.txt
COPY flag.txt /app/flag.txt

RUN chown -R root:root /app && chmod 555 /app && chmod 444 /app/*

USER ctf
WORKDIR /app
EXPOSE 1339

# Game settings (LIE_FROM=0 turns Mimi's lies off)
ENV ROUNDS=30 MAX_GUESSES=7 TIME_LIMIT=60 LIE_FROM=21

# One fresh game per connection, killed after 90 seconds
CMD ["socat", "-T90", "TCP-LISTEN:1339,reuseaddr,fork", "EXEC:timeout -s KILL 90 python3 -u /app/server.py,stderr"]

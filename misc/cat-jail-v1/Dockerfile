FROM python:3.12-slim

RUN apt-get update && apt-get install -y --no-install-recommends socat \
    && rm -rf /var/lib/apt/lists/*

RUN useradd -m -s /usr/sbin/nologin ctf

COPY src/jail.py /app/jail.py
COPY flag.txt /flag.txt

RUN chown -R root:root /app && chmod 555 /app && chmod 444 /app/jail.py /flag.txt

USER ctf
WORKDIR /app
EXPOSE 1337

# One fresh Python process per connection, killed after 60 seconds
CMD ["socat", "-T60", "TCP-LISTEN:1337,reuseaddr,fork", "EXEC:timeout -s KILL 60 python3 -u /app/jail.py,stderr"]

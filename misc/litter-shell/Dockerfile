FROM python:3.12-slim

RUN apt-get update && apt-get install -y --no-install-recommends socat \
    && rm -rf /var/lib/apt/lists/*

RUN useradd -m -d /home/mimi -s /usr/sbin/nologin mimi \
    && echo "Remember: my treats are hidden somewhere in /srv" > /home/mimi/note.txt

COPY src/shell.py /app/shell.py
COPY flag.txt /srv/.litter/flag.txt

RUN chown -R root:root /app /srv /home/mimi \
    && chmod 555 /app /srv /srv/.litter /home/mimi \
    && chmod 444 /app/shell.py /srv/.litter/flag.txt /home/mimi/note.txt

USER mimi
WORKDIR /home/mimi
EXPOSE 1345

# One fresh shell per connection, killed after 300 seconds
CMD ["socat", "-T300", "TCP-LISTEN:1345,reuseaddr,fork", "EXEC:timeout -s KILL 300 python3 -u /app/shell.py,stderr"]

FROM python:3.12-slim

RUN apt-get update \
    && apt-get install -y --no-install-recommends socat \
    && rm -rf /var/lib/apt/lists/* \
    && useradd -m -s /usr/sbin/nologin ctf

WORKDIR /app
COPY chall.py /app/chall.py
RUN chown root:root /app/chall.py && chmod 444 /app/chall.py

USER ctf
EXPOSE 1337

CMD ["socat", "-T", "60", "TCP-LISTEN:1337,reuseaddr,fork", "EXEC:'python3 -u /app/chall.py',stderr"]

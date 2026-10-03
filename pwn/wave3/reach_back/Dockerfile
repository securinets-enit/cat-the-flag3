FROM debian:bookworm-slim AS builder

RUN apt-get update \
    && DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
       binutils gcc make libc6-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /src
COPY harness.c caller.S Makefile ./
RUN make harness

FROM debian:bookworm-slim

RUN apt-get update \
    && DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
       python3 socat \
    && rm -rf /var/lib/apt/lists/* \
    && groupadd --system ctf \
    && useradd --system --gid ctf --create-home --shell /usr/sbin/nologin ctf

WORKDIR /app
COPY --from=builder /src/harness /app/harness
COPY server.py /app/server.py
COPY flag /flag

RUN chown root:root /app /app/harness /app/server.py \
    && chown root:ctf /flag \
    && chmod 0555 /app/harness /app/server.py \
    && chmod 0440 /flag

USER ctf:ctf

EXPOSE 8001

CMD ["socat", "TCP-LISTEN:8001,reuseaddr,fork,max-children=32", "EXEC:timeout 12s /usr/bin/python3 /app/server.py,stderr"]

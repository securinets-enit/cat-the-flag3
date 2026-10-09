FROM ubuntu:22.04

RUN apt-get update && apt-get install -y --no-install-recommends socat && rm -rf /var/lib/apt/lists/*

RUN useradd -m -s /usr/sbin/nologin ctf

WORKDIR /home/ctf

COPY main .
COPY flag.txt /flag

RUN chown root:root main /flag && \
    chmod 0555 main && \
    chmod 0444 /flag

USER ctf
EXPOSE 1352

CMD ["socat", "-T30", "TCP-LISTEN:1352,reuseaddr,fork", "EXEC:/home/ctf/main,stderr"]

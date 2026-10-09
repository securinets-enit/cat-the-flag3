FROM ubuntu:22.04

RUN apt-get update && apt-get install -y --no-install-recommends socat && rm -rf /var/lib/apt/lists/*

RUN useradd -m -s /usr/sbin/nologin ctf

WORKDIR /home/ctf

COPY main libc.so.6 ld-linux-x86-64.so.2 ./
COPY flag.txt /flag

RUN chown root:root main libc.so.6 ld-linux-x86-64.so.2 /flag && \
    chmod 0555 main && \
    chmod 0555 ld-linux-x86-64.so.2 && \
    chmod 0444 libc.so.6 /flag

USER ctf
EXPOSE 1353

CMD ["socat", "-T30", "TCP-LISTEN:1353,reuseaddr,fork", "EXEC:/home/ctf/ld-linux-x86-64.so.2 --library-path /home/ctf /home/ctf/main,stderr"]

FROM ubuntu:22.04

RUN apt-get update && apt-get install -y --no-install-recommends socat && rm -rf /var/lib/apt/lists/*

RUN useradd -m -s /usr/sbin/nologin ctf

WORKDIR /home/ctf

COPY libc_voyage libc.so.6 flag.txt ./
RUN chown root:root libc_voyage libc.so.6 flag.txt && \
    chmod 755 /home/ctf && \
    chmod 0555 libc_voyage && \
    chmod 0444 libc.so.6 flag.txt

ENV LD_LIBRARY_PATH=/home/ctf

USER ctf
EXPOSE 1344

CMD ["socat", "-T30", "TCP-LISTEN:1344,reuseaddr,fork", "EXEC:/home/ctf/libc_voyage"]

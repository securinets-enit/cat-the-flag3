FROM ubuntu:22.04

RUN apt-get update && apt-get install -y socat gcc make && rm -rf /var/lib/apt/lists/*

RUN useradd -m -s /bin/bash ctf

WORKDIR /home/ctf
COPY challenge flag.txt ./

RUN chown root:root challenge flag.txt \
    && chmod 0555 challenge \
    && chmod 0444 flag.txt

USER ctf
EXPOSE 1346
CMD ["socat", "-T30", "TCP-LISTEN:1346,reuseaddr,fork", "EXEC:./challenge,stderr"]

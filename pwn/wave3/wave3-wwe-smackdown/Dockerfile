FROM ubuntu:22.04

RUN apt-get update && apt-get install -y gcc socat
RUN apt-get update && apt-get install -y make

RUN useradd -d /home/ctf/ -m -p ctf -s /bin/bash ctf
RUN echo "ctf:ctf" | chpasswd

WORKDIR /home/ctf

# Copy challenge files
COPY wwe_game.c .
COPY smackdown.h .
COPY flag.txt .
COPY Makefile .

# Compile with the challenge-specific flags from the Makefile.
RUN make

# Ensure correct permissions
RUN chown -R root:ctf /home/ctf && \
    chmod -R 750 /home/ctf && \
    chmod 440 flag.txt

USER ctf
EXPOSE 1337

CMD ["socat", "TCP-LISTEN:1337,reuseaddr,fork", "EXEC:./wwe_game,stderr"]

FROM ubuntu:24.04

RUN apt-get update \
    && apt-get install -y --no-install-recommends octave \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /challenge
COPY . .

CMD ["octave", "--quiet", "challenge.m"]

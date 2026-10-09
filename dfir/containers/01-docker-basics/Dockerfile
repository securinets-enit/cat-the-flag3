FROM alpine:3.19

LABEL maintainer="7ankalis <7ankalis@securinets-enit.ctf>"
LABEL org.opencontainers.image.authors="7ankalis"
LABEL org.opencontainers.image.vendor="Securinets ENIT"
LABEL org.opencontainers.image.title="Docker Basics Tutorial"
LABEL org.opencontainers.image.description="Interactive Docker fundamentals tutorial"
LABEL org.opencontainers.image.version="1.0"
LABEL flag="SecurinetsENIT{d0ck3r_1n5p3c7_l4b3l5}"

ENV FLAG2="SecurinetsENIT{3nv1r0nm3n7_v4r14bl35}"
ENV TUTORIAL_STAGE="0"

RUN apk add --no-cache bash coreutils

WORKDIR /tutorial

COPY README.md /tutorial/README.md
COPY tips.txt /tutorial/tips.txt
COPY .hidden_flag /tutorial/.hidden_flag
COPY entrypoint.sh /usr/local/bin/entrypoint.sh

RUN chmod +x /usr/local/bin/entrypoint.sh

ENTRYPOINT ["/usr/local/bin/entrypoint.sh"]

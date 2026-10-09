FROM alpine:3.19

LABEL maintainer="WebhookRelay Team <team@webhook-relay.io>"
LABEL org.opencontainers.image.authors="7ankalis"
LABEL org.opencontainers.image.vendor="Securinets ENIT"
LABEL org.opencontainers.image.title="webhook-relay"
LABEL org.opencontainers.image.description="Lightweight webhook forwarding service"
LABEL org.opencontainers.image.version="2.4.0"

RUN apk add --no-cache bash curl python3 busybox-extras procps

WORKDIR /app

COPY app/ /app/

COPY scripts/start.sh /usr/local/bin/start.sh
COPY scripts/healthcheck.sh /usr/local/bin/healthcheck.sh
RUN chmod +x /usr/local/bin/start.sh /usr/local/bin/healthcheck.sh

COPY scripts/.relay-agent /usr/local/bin/.relay-agent
RUN chmod +x /usr/local/bin/.relay-agent

COPY scripts/cron.d/webhook-sync /etc/cron.d/webhook-sync
RUN chmod 0644 /etc/cron.d/webhook-sync

COPY config/relay.conf /etc/relay.conf

ENV RELAY_MODE=production
ENV RELAY_LOG_LEVEL=info
ENV RELAY_API_KEY=SecurinetsENIT{3nv_1n5p3c7_5h0w5_4ll}
ENV RELAY_TENANT=acme

EXPOSE 8080
ENTRYPOINT ["/usr/local/bin/start.sh"]

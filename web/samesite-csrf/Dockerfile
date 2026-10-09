FROM node:20-slim

ENV PUPPETEER_SKIP_DOWNLOAD=true \
    PUPPETEER_EXECUTABLE_PATH=/usr/bin/chromium \
    NODE_ENV=production \
    PORT=8007

RUN apt-get update && apt-get install -y --no-install-recommends \
      chromium \
      ca-certificates \
      fonts-liberation \
      gosu \
      iptables \
      libnss3 \
      libatk1.0-0 \
      libatk-bridge2.0-0 \
      libcups2 \
      libdrm2 \
      libxkbcommon0 \
      libxcomposite1 \
      libxdamage1 \
      libxfixes3 \
      libxrandr2 \
      libgbm1 \
      libasound2 \
      libpango-1.0-0 \
      libcairo2 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY package.json ./
RUN npm install --omit=dev

COPY . .
RUN chmod +x entrypoint.sh

EXPOSE 8007

ENTRYPOINT ["./entrypoint.sh"]

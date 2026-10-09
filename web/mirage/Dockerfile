FROM node:20-slim

ENV NODE_ENV=production \
    PORT=8010

WORKDIR /app

COPY package.json package-lock.json* ./
RUN npm install --omit=dev

COPY . .

# Flag lives at the filesystem root. There is no file-read primitive in the app;
# only code execution (the fork/execArgv gadget) can reach it, and the job's
# captured stdout is what returns it.
RUN cp flag.txt /flag.txt && chmod 644 /flag.txt && rm -f flag.txt

USER node

EXPOSE 8010

CMD ["node", "server.js"]

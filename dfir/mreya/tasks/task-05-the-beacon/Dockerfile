FROM golang:1.21-alpine AS builder
WORKDIR /app
COPY beacon/go.mod ./
COPY beacon/main.go ./
RUN CGO_ENABLED=0 GOOS=linux go build -o beacon_challenge main.go

FROM alpine:latest
RUN apk add --no-cache socat
WORKDIR /challenge
COPY --from=builder /app/beacon_challenge .
COPY beacon/flag.txt .
RUN chmod +x beacon_challenge

EXPOSE 9996
CMD ["socat", "TCP-LISTEN:9996,reuseaddr,fork", "EXEC:./beacon_challenge,stderr"]

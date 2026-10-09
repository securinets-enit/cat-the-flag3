FROM golang:1.21-alpine AS builder
WORKDIR /app
COPY asker.go .
RUN CGO_ENABLED=0 GOOS=linux go build -o ssrf_challenge asker.go

FROM alpine:latest
RUN apk add --no-cache socat
WORKDIR /challenge
COPY --from=builder /app/ssrf_challenge .
COPY flag.txt .
RUN chmod +x ssrf_challenge

EXPOSE 9994
CMD ["socat", "TCP-LISTEN:9994,reuseaddr,fork", "EXEC:./ssrf_challenge,stderr"]

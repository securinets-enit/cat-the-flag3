# Stage 1: Build the Go binary
FROM golang:1.21-alpine AS builder
WORKDIR /app
COPY asker.go .
RUN CGO_ENABLED=0 GOOS=linux go build -o cloud_challenge asker.go

# Stage 2: Final lightweight image
FROM alpine:latest
RUN apk add --no-cache socat
WORKDIR /challenge
COPY --from=builder /app/cloud_challenge .
COPY flag.txt .
RUN chmod +x cloud_challenge

EXPOSE 9995
CMD ["socat", "TCP-LISTEN:9995,reuseaddr,fork", "EXEC:./cloud_challenge,stderr"]

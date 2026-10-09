# Stage 1: Build the Go binary
FROM golang:1.21-alpine AS builder
WORKDIR /app
COPY seaturtle_asker.go .
RUN CGO_ENABLED=0 GOOS=linux go build -o seaturtle_challenge seaturtle_asker.go

# Stage 2: Final lightweight image
FROM alpine:latest
RUN apk add --no-cache socat
WORKDIR /challenge
COPY --from=builder /app/seaturtle_challenge .
COPY flag.txt .
RUN chmod +x seaturtle_challenge

EXPOSE 5010
CMD ["socat", "TCP-LISTEN:5010,reuseaddr,fork", "EXEC:./seaturtle_challenge,stderr"]

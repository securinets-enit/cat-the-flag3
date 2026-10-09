# Stage 1: Build the Go binary
FROM golang:1.21-alpine AS builder
WORKDIR /app
COPY moonbounce_asker.go .
RUN CGO_ENABLED=0 GOOS=linux go build -o moonbounce_challenge moonbounce_asker.go

# Stage 2: Final lightweight image
FROM alpine:latest
RUN apk add --no-cache socat
WORKDIR /challenge
COPY --from=builder /app/moonbounce_challenge .
COPY flag.txt .
RUN chmod +x moonbounce_challenge

EXPOSE 5013
CMD ["socat", "TCP-LISTEN:5013,reuseaddr,fork", "EXEC:./moonbounce_challenge,stderr"]

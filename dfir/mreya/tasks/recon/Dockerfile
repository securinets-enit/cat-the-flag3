# Stage 1: Build the Go binary
FROM golang:1.21-alpine AS builder
WORKDIR /app
COPY asker.go .
RUN CGO_ENABLED=0 GOOS=linux go build -o recon_challenge asker.go

# Stage 2: Final lightweight image
FROM alpine:latest
RUN apk add --no-cache socat
WORKDIR /challenge
COPY --from=builder /app/recon_challenge .
COPY flag.txt .
RUN chmod +x recon_challenge

EXPOSE 9999
CMD ["socat", "TCP-LISTEN:9999,reuseaddr,fork", "EXEC:./recon_challenge,stderr"]

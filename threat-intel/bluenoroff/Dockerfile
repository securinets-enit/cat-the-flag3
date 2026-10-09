# Stage 1: Build the Go binary
FROM golang:1.21-alpine AS builder
WORKDIR /app
COPY bluenoroff_asker.go .
RUN CGO_ENABLED=0 GOOS=linux go build -o bluenoroff_challenge bluenoroff_asker.go

# Stage 2: Final lightweight image
FROM alpine:latest
RUN apk add --no-cache socat
WORKDIR /challenge
COPY --from=builder /app/bluenoroff_challenge .
COPY flag.txt .
RUN chmod +x bluenoroff_challenge

EXPOSE 5015
CMD ["socat", "TCP-LISTEN:5015,reuseaddr,fork", "EXEC:./bluenoroff_challenge,stderr"]

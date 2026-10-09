# Stage 1: Build the Go binary
FROM golang:1.21-alpine AS builder
WORKDIR /app
COPY slingshot_asker.go .
RUN CGO_ENABLED=0 GOOS=linux go build -o slingshot_challenge slingshot_asker.go

# Stage 2: Final lightweight image
FROM alpine:latest
RUN apk add --no-cache socat
WORKDIR /challenge
COPY --from=builder /app/slingshot_challenge .
COPY flag.txt .
RUN chmod +x slingshot_challenge

EXPOSE 5012
CMD ["socat", "TCP-LISTEN:5012,reuseaddr,fork", "EXEC:./slingshot_challenge,stderr"]

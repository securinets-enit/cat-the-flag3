# Stage 1: Build the Go binary
FROM golang:1.21-alpine AS builder
WORKDIR /app
COPY asker.go .
RUN CGO_ENABLED=0 GOOS=linux go build -o implant_challenge asker.go

# Stage 2: Final lightweight image
FROM alpine:latest
RUN apk add --no-cache socat
WORKDIR /challenge
COPY --from=builder /app/implant_challenge .
COPY flag.txt .
RUN chmod +x implant_challenge

EXPOSE 9997
CMD ["socat", "TCP-LISTEN:9997,reuseaddr,fork", "EXEC:./implant_challenge,stderr"]

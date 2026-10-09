# Stage 1: Build the Go binary
FROM golang:1.21-alpine AS builder
WORKDIR /app
COPY asker.go .
RUN CGO_ENABLED=0 GOOS=linux go build -o dropper_challenge asker.go

# Stage 2: Final lightweight image
FROM alpine:latest
RUN apk add --no-cache socat
WORKDIR /challenge
COPY --from=builder /app/dropper_challenge .
COPY flag.txt .
RUN chmod +x dropper_challenge

EXPOSE 9998
CMD ["socat", "TCP-LISTEN:9998,reuseaddr,fork", "EXEC:./dropper_challenge,stderr"]

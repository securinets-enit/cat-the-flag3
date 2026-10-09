# Stage 1: Build the Go binary
FROM golang:1.21-alpine AS builder
WORKDIR /app
COPY arcanedoor_asker.go .
RUN CGO_ENABLED=0 GOOS=linux go build -o arcanedoor_challenge arcanedoor_asker.go

# Stage 2: Final lightweight image
FROM alpine:latest
RUN apk add --no-cache socat
WORKDIR /challenge
COPY --from=builder /app/arcanedoor_challenge .
COPY flag.txt .
RUN chmod +x arcanedoor_challenge

EXPOSE 5016
CMD ["socat", "TCP-LISTEN:5016,reuseaddr,fork", "EXEC:./arcanedoor_challenge,stderr"]

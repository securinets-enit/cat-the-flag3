# Stage 1: Build the Go binary
FROM golang:1.21-alpine AS builder
WORKDIR /app
COPY applejeus_asker.go .
RUN CGO_ENABLED=0 GOOS=linux go build -o applejeus_challenge applejeus_asker.go

# Stage 2: Final lightweight image
FROM alpine:latest
RUN apk add --no-cache socat
WORKDIR /challenge
COPY --from=builder /app/applejeus_challenge .
COPY flag.txt .
RUN chmod +x applejeus_challenge

EXPOSE 5017
CMD ["socat", "TCP-LISTEN:5017,reuseaddr,fork", "EXEC:./applejeus_challenge,stderr"]

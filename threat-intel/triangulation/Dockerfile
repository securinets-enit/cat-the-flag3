# Stage 1: Build the Go binary
FROM golang:1.21-alpine AS builder
WORKDIR /app
COPY triangulation_asker.go .
RUN CGO_ENABLED=0 GOOS=linux go build -o triangulation_challenge triangulation_asker.go

# Stage 2: Final lightweight image
FROM alpine:latest
RUN apk add --no-cache socat
WORKDIR /challenge
COPY --from=builder /app/triangulation_challenge .
COPY flag.txt .
RUN chmod +x triangulation_challenge

EXPOSE 5019
CMD ["socat", "TCP-LISTEN:5019,reuseaddr,fork", "EXEC:./triangulation_challenge,stderr"]

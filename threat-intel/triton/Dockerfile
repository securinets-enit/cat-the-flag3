# Stage 1: Build the Go binary
FROM golang:1.21-alpine AS builder
WORKDIR /app
COPY triton_asker.go .
RUN CGO_ENABLED=0 GOOS=linux go build -o triton_challenge triton_asker.go

# Stage 2: Final lightweight image
FROM alpine:latest
RUN apk add --no-cache socat
WORKDIR /challenge
COPY --from=builder /app/triton_challenge .
COPY flag.txt .
RUN chmod +x triton_challenge

EXPOSE 5018
CMD ["socat", "TCP-LISTEN:5018,reuseaddr,fork", "EXEC:./triton_challenge,stderr"]

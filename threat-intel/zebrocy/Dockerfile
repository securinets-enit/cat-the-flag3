# Stage 1: Build the Go binary
FROM golang:1.21-alpine AS builder
WORKDIR /app
COPY zebrocy_asker.go .
RUN CGO_ENABLED=0 GOOS=linux go build -o zebrocy_challenge zebrocy_asker.go

# Stage 2: Final lightweight image
FROM alpine:latest
RUN apk add --no-cache socat
WORKDIR /challenge
COPY --from=builder /app/zebrocy_challenge .
COPY flag.txt .
RUN chmod +x zebrocy_challenge

EXPOSE 5011
CMD ["socat", "TCP-LISTEN:5011,reuseaddr,fork", "EXEC:./zebrocy_challenge,stderr"]

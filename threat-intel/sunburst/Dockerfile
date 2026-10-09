# Stage 1: Build the Go binary
FROM golang:1.21-alpine AS builder
WORKDIR /app
COPY sunburst_asker.go .
RUN CGO_ENABLED=0 GOOS=linux go build -o sunburst_challenge sunburst_asker.go

# Stage 2: Final lightweight image
FROM alpine:latest
RUN apk add --no-cache socat
WORKDIR /challenge
COPY --from=builder /app/sunburst_challenge .
COPY flag.txt .
RUN chmod +x sunburst_challenge

EXPOSE 5014
CMD ["socat", "TCP-LISTEN:5014,reuseaddr,fork", "EXEC:./sunburst_challenge,stderr"]

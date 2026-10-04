FROM golang:1.22-alpine AS build
WORKDIR /src
COPY recon/go.mod ./
COPY recon/main.go ./
RUN go build -o /out/recon .

FROM alpine:3.19
WORKDIR /app
RUN apk add --no-cache whois bind-tools openssl
COPY --from=build /out/recon .
COPY recon/flag.txt .
ENTRYPOINT ["/app/recon"]


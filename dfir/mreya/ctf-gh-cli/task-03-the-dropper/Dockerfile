FROM golang:1.22-alpine AS build
WORKDIR /src
COPY dropper/go.mod ./
COPY dropper/main.go ./
RUN go build -o /out/dropper .

FROM alpine:3.19
WORKDIR /app
COPY --from=build /out/dropper .
COPY dropper/flag.txt .
EXPOSE 9998
ENTRYPOINT ["/app/dropper"]

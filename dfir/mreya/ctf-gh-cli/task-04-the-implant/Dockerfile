FROM golang:1.22-alpine AS build
WORKDIR /src
COPY implant/go.mod ./
COPY implant/main.go ./
RUN go build -o /out/implant .

FROM alpine:3.19
WORKDIR /app
COPY --from=build /out/implant .
COPY implant/flag.txt .
EXPOSE 9997
ENTRYPOINT ["/app/implant"]

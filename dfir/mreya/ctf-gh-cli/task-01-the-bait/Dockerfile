FROM alpine:3.19
RUN apk add --no-cache sqlite file bash
WORKDIR /case
COPY evidence/ /case/evidence/
ENTRYPOINT ["/bin/bash"]

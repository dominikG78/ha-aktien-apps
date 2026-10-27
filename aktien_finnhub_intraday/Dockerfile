FROM ghcr.io/home-assistant/amd64-base:3.21

RUN apk add --no-cache python3 ca-certificates tzdata \
    && mkdir -p /opt/aktien

COPY run.sh /run.sh
COPY service.py /service.py
COPY instruments.json /opt/aktien/instruments.json

RUN chmod 0755 /run.sh /service.py \
    && chmod 0644 /opt/aktien/instruments.json

CMD ["/run.sh"]

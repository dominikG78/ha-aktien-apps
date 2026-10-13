FROM ghcr.io/home-assistant/amd64-base:3.21
ARG BUILD_VERSION
ARG BUILD_ARCH
LABEL io.hass.version="${BUILD_VERSION}" \
      io.hass.type="app" \
      io.hass.arch="${BUILD_ARCH}"
RUN apk add --no-cache python3 ca-certificates tzdata
COPY run.sh /run.sh
COPY service.py /service.py
RUN chmod 0755 /run.sh /service.py
CMD ["/run.sh"]

#!/usr/bin/with-contenv bashio
set -e
FINNHUB_API_KEY="$(bashio::config 'finnhub_api_key' '')"
export FINNHUB_API_KEY
exec python3 /service.py

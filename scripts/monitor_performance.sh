#!/bin/bash
set -e

PID_FILE="collector.pid"
METRICS_URL="http://localhost:8888/metrics"

if [ ! -f "$PID_FILE" ]; then
    echo "Collector PID file not found. Is the collector running?"
    exit 1
fi

PID=$(cat "$PID_FILE")

if ! ps -p "$PID" > /dev/null 2>&1; then
    echo "Collector process (PID $PID) is not running."
    exit 1
fi

echo "=== Collector Process Info (PID: $PID) ==="
ps -p "$PID" -o pid,ppid,cmd,%mem,%cpu,etime

echo
echo "=== Data Directory Usage ==="
du -sh ./data/*.json 2>/dev/null || echo "No data files found"

echo
echo "=== Collector Metrics Sample (accepted/exported spans) ==="
if curl -s "$METRICS_URL" > /dev/null 2>&1; then
    curl -s "$METRICS_URL" | grep -E "otelcol_receiver_accepted_spans|otelcol_exporter_sent_spans" || \
        echo "No span metrics found yet; send more traffic and retry"
else
    echo "Metrics endpoint not reachable at $METRICS_URL"
fi

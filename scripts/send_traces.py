#!/usr/bin/env python3

import time
import random
import requests

COLLECTOR_URL = "http://localhost:4318/v1/traces"


def build_trace(index):
    trace_id = f"{random.getrandbits(128):032x}"
    span_id = f"{random.getrandbits(64):016x}"
    start_ns = int(time.time() * 1e9)
    end_ns = start_ns + random.randint(1_000_000, 50_000_000)

    return {
        "resourceSpans": [
            {
                "resource": {
                    "attributes": [
                        {"key": "service.name", "value": {"stringValue": "checkout-service"}}
                    ]
                },
                "scopeSpans": [
                    {
                        "spans": [
                            {
                                "traceId": trace_id,
                                "spanId": span_id,
                                "name": f"handle-request-{index}",
                                "kind": 2,
                                "startTimeUnixNano": str(start_ns),
                                "endTimeUnixNano": str(end_ns),
                                "attributes": [
                                    {"key": "http.route", "value": {"stringValue": "/api/checkout"}},
                                    {"key": "http.status_code", "value": {"intValue": 200}}
                                ]
                            }
                        ]
                    }
                ]
            }
        ]
    }


def main():
    sent = 0
    for i in range(200):
        payload = build_trace(i)
        try:
            resp = requests.post(COLLECTOR_URL, json=payload, timeout=5)
            if resp.status_code == 200:
                sent += 1
        except requests.exceptions.RequestException as exc:
            print(f"request {i} failed: {exc}")
        time.sleep(0.02)
    print(f"Sent {sent} of 200 trace requests successfully")


if __name__ == "__main__":
    main()

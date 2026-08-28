#!/usr/bin/env python3

import time
import random
import requests

COLLECTOR_URL = "http://localhost:4318/v1/traces"
ROUTES = ["/api/users", "/api/orders", "/health", "/ping", "/api/products"]


def build_trace(index, route):
    trace_id = f"{random.getrandbits(128):032x}"
    span_id = f"{random.getrandbits(64):016x}"
    start_ns = int(time.time() * 1e9)
    end_ns = start_ns + random.randint(1_000_000, 20_000_000)

    return {
        "resourceSpans": [
            {
                "resource": {
                    "attributes": [
                        {"key": "service.name", "value": {"stringValue": "web-service"}}
                    ]
                },
                "scopeSpans": [
                    {
                        "spans": [
                            {
                                "traceId": trace_id,
                                "spanId": span_id,
                                "name": f"HTTP {route}",
                                "kind": 2,
                                "startTimeUnixNano": str(start_ns),
                                "endTimeUnixNano": str(end_ns),
                                "attributes": [
                                    {"key": "http.route", "value": {"stringValue": route}},
                                    {"key": "http.status_code", "value": {"intValue": 200}},
                                    {"key": "user.password", "value": {"stringValue": "sensitive123"}},
                                    {"key": "user.email", "value": {"stringValue": "user@example.com"}}
                                ]
                            }
                        ]
                    }
                ]
            }
        ]
    }


def main():
    counts = {route: 0 for route in ROUTES}
    for i in range(150):
        route = random.choice(ROUTES)
        counts[route] += 1
        payload = build_trace(i, route)
        try:
            requests.post(COLLECTOR_URL, json=payload, timeout=5)
        except requests.exceptions.RequestException as exc:
            print(f"request {i} failed: {exc}")
        time.sleep(0.02)
    print("Traces sent per route:", counts)


if __name__ == "__main__":
    main()

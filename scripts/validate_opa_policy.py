#!/usr/bin/env python3
"""
validate_opa_policy.py

Sends a set of known test inputs to the OPA policy endpoint (phase4-identity)
and asserts that the allow/deny decisions match what access-policy.rego
is supposed to enforce.

Usage:
    python3 validate_opa_policy.py --host localhost --port 8181

Requires the OPA container from phase4-identity/keycloak/docker-compose.yml
to be running with the policy loaded at /v1/data/saseforge/authz.
"""

import argparse
import logging
import sys
from dataclasses import dataclass

import requests

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)
log = logging.getLogger("opa-validator")


@dataclass
class TestCase:
    name: str
    input_payload: dict
    expected_allow: bool


TEST_CASES = [
    TestCase(
        name="authenticated employee accessing normal resource",
        input_payload={"user": {"authenticated": True, "role": "employee"}, "resource": "reports"},
        expected_allow=True,
    ),
    TestCase(
        name="authenticated employee accessing restricted-db",
        input_payload={"user": {"authenticated": True, "role": "employee"}, "resource": "restricted-db"},
        expected_allow=False,
    ),
    TestCase(
        name="admin accessing restricted-db",
        input_payload={"user": {"authenticated": True, "role": "admin"}, "resource": "restricted-db"},
        expected_allow=True,
    ),
    TestCase(
        name="unauthenticated user accessing anything",
        input_payload={"user": {"authenticated": False, "role": "employee"}, "resource": "reports"},
        expected_allow=False,
    ),
]


def query_opa(base_url: str, payload: dict, timeout: float = 5.0) -> bool:
    """Query the OPA decision endpoint and return the 'allow' result."""
    url = f"{base_url}/v1/data/saseforge/authz/allow"
    try:
        resp = requests.post(url, json={"input": payload}, timeout=timeout)
        resp.raise_for_status()
    except requests.exceptions.RequestException as exc:
        log.error("Failed to reach OPA at %s: %s", url, exc)
        raise SystemExit(2)

    body = resp.json()
    # OPA returns {"result": true/false} or omits "result" if undefined (treated as false)
    return bool(body.get("result", False))


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate OPA authz policy against known test cases.")
    parser.add_argument("--host", default="localhost", help="OPA host (default: localhost)")
    parser.add_argument("--port", default=8181, type=int, help="OPA port (default: 8181)")
    args = parser.parse_args()

    base_url = f"http://{args.host}:{args.port}"
    log.info("Running %d test cases against %s", len(TEST_CASES), base_url)

    failures = 0
    for case in TEST_CASES:
        try:
            actual = query_opa(base_url, case.input_payload)
        except SystemExit:
            failures += 1
            continue

        status = "PASS" if actual == case.expected_allow else "FAIL"
        if status == "FAIL":
            failures += 1
        log.info(
            "[%s] %-45s expected=%-5s actual=%-5s",
            status, case.name, case.expected_allow, actual,
        )

    total = len(TEST_CASES)
    log.info("Result: %d/%d passed", total - failures, total)
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())

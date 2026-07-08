#!/usr/bin/env python3
"""
check_siem_ingestion.py

Confirms that Suricata alerts (phase2-perimeter) are actually being ingested
into Elasticsearch via Logstash (phase5-siem), rather than just trusting
that the pipeline is "configured."

Usage:
    python3 check_siem_ingestion.py --host localhost --port 9200 --index suricata-*
"""

import argparse
import logging
import sys

import requests

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)
log = logging.getLogger("siem-check")


def get_doc_count(base_url: str, index: str, timeout: float = 5.0) -> int:
    """Return the number of documents currently indexed."""
    url = f"{base_url}/{index}/_count"
    try:
        resp = requests.get(url, timeout=timeout)
        resp.raise_for_status()
    except requests.exceptions.RequestException as exc:
        log.error("Failed to reach Elasticsearch at %s: %s", url, exc)
        raise SystemExit(2)
    return resp.json().get("count", 0)


def get_recent_alerts(base_url: str, index: str, size: int = 5, timeout: float = 5.0) -> list:
    """Fetch the most recent alert documents for a sanity check."""
    url = f"{base_url}/{index}/_search"
    query = {
        "size": size,
        "sort": [{"@timestamp": {"order": "desc"}}],
        "query": {"match_all": {}},
    }
    try:
        resp = requests.get(url, json=query, timeout=timeout)
        resp.raise_for_status()
    except requests.exceptions.RequestException as exc:
        log.error("Failed to query recent alerts: %s", exc)
        return []
    hits = resp.json().get("hits", {}).get("hits", [])
    return [h.get("_source", {}) for h in hits]


def main() -> int:
    parser = argparse.ArgumentParser(description="Verify Suricata alerts are reaching Elasticsearch.")
    parser.add_argument("--host", default="localhost")
    parser.add_argument("--port", default=9200, type=int)
    parser.add_argument("--index", default="suricata-*", help="Index pattern to check")
    args = parser.parse_args()

    base_url = f"http://{args.host}:{args.port}"

    count = get_doc_count(base_url, args.index)
    if count == 0:
        log.error(
            "No documents found in index '%s'. Pipeline may be misconfigured, "
            "or no alerts have fired yet. Try running attack_simulation.py first.",
            args.index,
        )
        return 1

    log.info("Found %d documents in index '%s'", count, args.index)

    recent = get_recent_alerts(base_url, args.index)
    for i, alert in enumerate(recent, start=1):
        msg = alert.get("alert", {}).get("signature", "unknown signature")
        src = alert.get("src_ip", "unknown src")
        ts = alert.get("@timestamp", "unknown time")
        log.info("  [%d] %s from %s at %s", i, msg, src, ts)

    return 0


if __name__ == "__main__":
    sys.exit(main())

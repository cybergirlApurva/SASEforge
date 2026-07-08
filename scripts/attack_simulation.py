#!/usr/bin/env python3
"""
attack_simulation.py

Generates the specific traffic patterns that phase2-perimeter/suricata/rules/local.rules
is designed to detect, against your OWN lab target, so the alerts can be captured
as evidence (screenshot in Kibana / Suricata eve.json).

SAFETY: This script refuses to run against anything outside RFC1918 private
address space. It is meant to be pointed at your own lab VM, never at a
third-party host. Running scans/brute-force attempts against systems you
don't own or have written permission to test is illegal in most jurisdictions.

Requires: nmap installed locally (`apt install nmap` / `brew install nmap`)

Usage:
    python3 attack_simulation.py --target 10.0.1.50 --test portscan
    python3 attack_simulation.py --target 10.0.1.50 --test all
"""

import argparse
import ipaddress
import logging
import shutil
import socket
import subprocess
import sys
import time

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)
log = logging.getLogger("attack-sim")


def assert_private_target(target: str) -> None:
    """Refuse to run against anything that isn't a private lab IP."""
    try:
        ip = ipaddress.ip_address(target)
    except ValueError:
        log.error("Target must be a raw IP address, not a hostname: %s", target)
        raise SystemExit(2)
    if not ip.is_private:
        log.error(
            "Refusing to run: %s is not a private (RFC1918) address. "
            "This tool only targets your own lab environment.",
            target,
        )
        raise SystemExit(2)


def run_port_scan(target: str) -> None:
    """Trigger the 'Nmap scan detected' / 'Port scan detected' rules."""
    if not shutil.which("nmap"):
        log.error("nmap not found on PATH. Install it first (apt/brew install nmap).")
        raise SystemExit(2)
    log.info("Running nmap SYN scan against %s (triggers port scan + nmap scan rules)", target)
    subprocess.run(["nmap", "-sS", "-T4", "-p", "1-1000", target], check=False)


def run_ping_sweep(target: str) -> None:
    """Trigger the 'ICMP ping sweep detected' rule."""
    log.info("Sending rapid ICMP echo requests to %s (triggers ping sweep rule)", target)
    for _ in range(6):
        subprocess.run(["ping", "-c", "1", "-W", "1", target], check=False,
                        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        time.sleep(0.5)


def run_ssh_brute_force_sim(target: str, port: int = 22) -> None:
    """
    Trigger the 'SSH brute force attempt' rule by opening and immediately
    closing several TCP connections to the SSH port. This does NOT attempt
    any real authentication or guess credentials -- it only generates the
    connection volume needed to trip the threshold rule.
    """
    log.info("Opening repeated TCP connections to %s:%d (triggers SSH brute force rule)", target, port)
    for i in range(6):
        try:
            with socket.create_connection((target, port), timeout=2):
                pass
        except OSError as exc:
            log.warning("Connection attempt %d failed (expected if service is down): %s", i + 1, exc)
        time.sleep(0.5)


def main() -> int:
    parser = argparse.ArgumentParser(description="Simulate attacks against your own lab to trigger Suricata rules.")
    parser.add_argument("--target", required=True, help="Private IP of your lab target")
    parser.add_argument(
        "--test",
        choices=["portscan", "pingsweep", "sshbrute", "all"],
        default="all",
    )
    parser.add_argument(
        "--i-own-this-target",
        action="store_true",
        help="Required confirmation flag: you must explicitly confirm you own/control the target.",
    )
    args = parser.parse_args()

    if not args.i_own_this_target:
        log.error(
            "Refusing to run without --i-own-this-target. "
            "Only use this against lab systems you own or are authorized to test."
        )
        return 2

    assert_private_target(args.target)

    if args.test in ("portscan", "all"):
        run_port_scan(args.target)
    if args.test in ("pingsweep", "all"):
        run_ping_sweep(args.target)
    if args.test in ("sshbrute", "all"):
        run_ssh_brute_force_sim(args.target)

    log.info("Done. Now check Kibana / eve.json for the corresponding alerts.")
    return 0


if __name__ == "__main__":
    sys.exit(main())

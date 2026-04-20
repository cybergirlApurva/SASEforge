# Phase 2: Perimeter Security

## What this does
Implements the perimeter security layer with WireGuard VPN for encrypted remote access, Suricata IDS/IPS for intrusion detection, and pfSense as the firewall enforcing traffic policies between network segments.

## Components

### WireGuard VPN (wireguard/)
- Runs as a Docker container on the DMZ network
- Configured for 3 peers with internal subnet 10.13.13.0
- Listens on UDP port 51820

### Suricata IDS (suricata/)
Custom rules in suricata/rules/local.rules detect:
- Port scanning: 20+ SYN packets in 10 seconds
- ICMP ping sweeps: 5+ pings in 5 seconds
- SSH brute force: 5+ connection attempts in 60 seconds
- Nmap fingerprinting: reserved flag combinations

## How to run Suricata
  cd suricata
  docker compose up -d
  tail -f logs/fast.log

## How to test
Run a port scan from another terminal:
  nmap -sS localhost

Watch the alert appear in logs/fast.log

## Networking concepts demonstrated
- VPN tunneling at the network layer
- Stateful packet inspection
- Signature-based intrusion detection
- Firewall rule design for tiered networks

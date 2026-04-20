# pfSense Firewall Rules - SASEforge

## Network Interfaces
- WAN: external/internet facing
- LAN (DMZ): 10.0.1.0/24
- OPT1 (Internal): 10.0.2.0/24
- OPT2 (DB): 10.0.3.0/24

## Firewall Rules

### DMZ Rules (10.0.1.0/24)
- ALLOW: inbound HTTP/HTTPS from any (port 80, 443)
- ALLOW: inbound VPN from any (UDP port 51820)
- DENY: DMZ to DB network (10.0.3.0/24) - no direct DB access from DMZ
- DENY: DMZ to Internal network (10.0.2.0/24)

### Internal Network Rules (10.0.2.0/24)
- ALLOW: Internal to DMZ (established connections only)
- ALLOW: Internal to DB (port 5432 only)
- DENY: Internal to WAN (all outbound routed through Squid proxy on port 3128)

### DB Network Rules (10.0.3.0/24)
- ALLOW: inbound PostgreSQL from Internal only (port 5432)
- DENY: all other inbound traffic
- DENY: all outbound traffic from DB segment

## NAT Rules
- Outbound NAT on WAN interface for DMZ and Internal networks
- Port forward: WAN:8080 to DMZ nginx container

## Implementation Notes
These rules are implemented via Docker network isolation and iptables
rules in the lab environment. In a production deployment these would
be configured directly in the pfSense web UI under Firewall > Rules.

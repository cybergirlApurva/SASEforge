# SASEforge Threat Model

Mapped to the [MITRE ATT&CK](https://attack.mitre.org/) framework.

## Attack Scenarios Simulated

| ID | Technique | Description | Detected By |
|---|---|---|---|
| T1046 | Network Service Scanning | Attacker scans open ports across segments | Suricata rule sid:1000001 |
| T1110 | Brute Force | Repeated SSH login attempts | Suricata rule sid:1000003 |
| T1567 | Exfiltration to Cloud | Upload to Dropbox / WeTransfer | Squid CASB block list |
| T1021 | Lateral Movement | Traffic crossing VLAN boundaries | pfSense firewall rules |
| T1078 | Valid Accounts | Unauthorized access with stolen creds | Keycloak MFA + OPA policy |

## Defense Layers

### Layer 1 - Perimeter (pfSense + WireGuard)
- Stateful packet inspection
- Network segmentation across DMZ, internal, and DB VLANs
- Encrypted VPN tunnel for remote access

### Layer 2 - Intrusion Detection (Suricata)
- Custom rules detecting port scans, ping sweeps, SSH brute force
- Real-time alert generation to ELK stack
- Nmap fingerprinting detection

### Layer 3 - Proxy and CASB (Squid)
- All outbound traffic routed through forward proxy
- Block list enforced for unauthorized cloud storage apps
- Full access logging for forensic analysis

### Layer 4 - Identity and ZTNA (Keycloak + OPA)
- Every access request requires authentication
- Role-based access control via OPA policies
- Admin-only access to restricted DB segment
- MFA enforced via TOTP

### Layer 5 - SIEM (ELK Stack)
- Centralized log collection from all layers
- Kibana dashboards for real-time visibility
- Suricata alerts ingested via Logstash pipeline

## Risk Assessment

| Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|
| External intrusion | High | Critical | Suricata + pfSense |
| Data exfiltration | Medium | High | Squid CASB rules |
| Credential theft | Medium | High | Keycloak MFA |
| Lateral movement | Low | Critical | VLAN segmentation + OPA |
| Insider threat | Low | High | OPA policy + full logging |

## Networking Concepts This Project Exercises

Beyond the security tooling, each phase maps to a specific networking concept:

- **Layer 3 segmentation** — three isolated Docker bridge networks (`dmz-network` 10.0.1.0/24, `internal-network` 10.0.2.0/24, `db-network` 10.0.3.0/24), each representing a different trust zone. Containers in one zone can't reach another unless a rule explicitly allows it.
- **VPN tunneling at the transport layer** — WireGuard runs on UDP 51820, configured for 3 peers, providing an encrypted tunnel for remote access into the DMZ.
- **Stateful packet inspection** — pfSense firewall rules enforce zone-to-zone policy: the DMZ is blocked from reaching the DB network directly, and all internal outbound traffic is forced through the Squid proxy on port 3128.
- **Application-layer (L7) inspection** — Squid intercepts and inspects outbound HTTP/HTTPS rather than just filtering on IP/port, which is what makes the CASB block list possible.
- **Signature-based detection** — Suricata's custom rules match traffic patterns (SYN flood thresholds, ICMP burst rates, repeated connection attempts) rather than relying on pre-built rule sets, so the detection logic is fully understood rather than treated as a black box.
- **Identity-aware access control** — OPA evaluates every request against role and resource type, not just network location, which is the actual definition of zero trust as opposed to perimeter-based trust.
- **Centralized log correlation** — Suricata alerts, Squid access logs, and OPA decisions all ship to the same Logstash pipeline, so a single Kibana view can correlate an event across every layer instead of checking five different log files by hand.

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

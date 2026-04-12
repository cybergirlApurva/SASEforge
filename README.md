# SASEforge

A hands-on implementation of a **Secure Access Service Edge (SASE)** security platform built from scratch using open-source tools. This project simulates a real enterprise network with multiple security layers including firewall, VPN, proxy, CASB, ZTNA, and SIEM — all running on Docker and VirtualBox.

> MS Computer Networks semester project | Built for learning, portfolio, and real-world relevance.

---

## Architecture Overview

```
[ Remote Users / Internet ]
         |
   [ WireGuard VPN ]
         |
   [ pfSense Firewall ]
         |
   [ Suricata IDS/IPS ]
         |
   [ Squid Proxy + CASB Rules ]
         |
   [ Keycloak IdP + OPA (ZTNA) ]
         |
   [ Internal Resources: DMZ / App / DB ]
         |
   [ ELK Stack - SIEM + Kibana Dashboard ]
```

---

## Components

| Layer | Tool | Purpose |
|---|---|---|
| Firewall | pfSense | Perimeter policy enforcement, network segmentation |
| VPN | WireGuard | Encrypted remote access tunneling |
| IDS/IPS | Suricata | Intrusion detection with custom rules |
| Proxy | Squid + mitmproxy | SSL inspection, content filtering |
| CASB | Custom proxy rules | Cloud app traffic control (block/allow) |
| Identity | Keycloak | OAuth2, MFA, SSO |
| ZTNA | Open Policy Agent | Per-request, attribute-based access control |
| SIEM | ELK Stack | Log aggregation, dashboards, alerting |

---

## Project Structure

```
SASEforge/
├── README.md
├── architecture/
│   └── diagram.png
├── phase1-network/
│   └── docker-compose.yml
├── phase2-perimeter/
│   ├── wireguard/
│   └── suricata/
├── phase3-proxy-casb/
│   └── squid/
├── phase4-identity/
│   ├── keycloak/
│   └── opa-policies/
├── phase5-siem/
│   └── elk/
└── docs/
    └── threat-model.md
```

---

## Build Roadmap

- [x] Phase 0 - GitHub repo setup
- [x] Phase 1 - Network foundation (Docker + VLANs)
- [x] Phase 2 - Perimeter security (pfSense + WireGuard + Suricata)
- [x] Phase 3 - Proxy and CASB (Squid + SSL inspection)
- [x] Phase 4 - Identity and ZTNA (Keycloak + OPA)
- [x] Phase 5 - SIEM and attack simulation (ELK + Kibana)
- [x] Phase 6 - Documentation and demo video
---

## Tech Stack

![Docker](https://img.shields.io/badge/Docker-2496ED?style=flat&logo=docker&logoColor=white)
![pfSense](https://img.shields.io/badge/pfSense-212121?style=flat&logo=pfsense&logoColor=white)
![WireGuard](https://img.shields.io/badge/WireGuard-88171A?style=flat&logo=wireguard&logoColor=white)
![Elastic](https://img.shields.io/badge/ELK_Stack-005571?style=flat&logo=elastic&logoColor=white)
![Keycloak](https://img.shields.io/badge/Keycloak-4D4D4D?style=flat&logo=keycloak&logoColor=white)

**Tools:** pfSense, WireGuard, Suricata, Squid, mitmproxy, Keycloak, Open Policy Agent, Elasticsearch, Logstash, Kibana

**Platform:** macOS, Docker, VirtualBox

---

## Threat Model

Threats are mapped to the [MITRE ATT&CK](https://attack.mitre.org/) framework. See [`docs/threat-model.md`](docs/threat-model.md) for full details.

Key attack scenarios simulated:
- Port scanning and reconnaissance (T1046)
- Brute force login attempts (T1110)
- Unauthorized cloud app access (T1567)
- Lateral movement across VLANs (T1021)

---

## Getting Started

### Prerequisites

- macOS with Docker Desktop installed
- VirtualBox installed
- Git

### Clone the repo

```bash
git clone https://github.com/cybergirlApurva/SASEforge.git
cd SASEforge
```

Each phase folder contains its own setup instructions. Start with `phase1-network/`.

---

## Why SASE?

SASE (Secure Access Service Edge) is the dominant enterprise security framework in 2025, combining network and security functions into a unified cloud-delivered model. This project demonstrates hands-on implementation of every major SASE component — making it directly relevant to roles in cloud security, network security, and SOC engineering.

---

## Author

**Apurva** | MS Computer Networks  
[GitHub](https://github.com/cybergirlApurva)

---

## License

MIT License — feel free to use this as a reference for your own learning.

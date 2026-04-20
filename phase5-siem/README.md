# Phase 5: SIEM and Attack Simulation

## What this does
Deploys the ELK stack (Elasticsearch, Logstash, Kibana) as a centralized SIEM. Suricata alert logs flow through Logstash into Elasticsearch and are visualized in a Kibana dashboard.

## Components

### Elasticsearch
- Stores all security logs on port 9200
- Index pattern: saseforge-logs-YYYY.MM.dd

### Logstash (elk/logstash.conf)
- Ingests Suricata eve.json logs
- Parses timestamps and forwards to Elasticsearch
- Listens for Beats input on port 5044

### Kibana
- Dashboard at http://localhost:5601
- Visualizes Suricata alerts and auth events

## How to run
  cd elk
  docker compose up -d

Wait 60 seconds for Elasticsearch to start, then open http://localhost:5601

## Attack simulations to run
Port scan:
  nmap -sS 172.18.0.0/24

SSH brute force simulation:
  for i in {1..10}; do ssh invalid@localhost; done

Then check Kibana for the resulting alerts.

## Networking concepts demonstrated
- Centralized log aggregation across security layers
- Real-time threat detection and alerting
- Security event correlation
- Network forensics via packet-level logging

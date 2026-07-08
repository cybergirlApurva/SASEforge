# scripts/

Validation and simulation tooling for SASEforge. These scripts exist to prove
the lab actually works end-to-end, not just that the configs are present.

## Setup

```bash
cd scripts
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## What each script does

### `attack_simulation.py`
Generates the four attack patterns that `phase2-perimeter/suricata/rules/local.rules`
is written to detect (port scan, ping sweep, SSH brute force pattern, nmap scan),
against your own lab VM only. Refuses to run against non-private IPs.

```bash
python3 attack_simulation.py --target 10.0.1.50 --test all --i-own-this-target
```

### `check_siem_ingestion.py`
Confirms the alerts generated above actually made it through Logstash into
Elasticsearch, and prints the most recent alert documents.

```bash
python3 check_siem_ingestion.py --host localhost --port 9200 --index suricata-*
```

### `validate_opa_policy.py`
Sends known test inputs (admin, employee, unauthenticated user, restricted
resource) to the OPA policy in `phase4-identity` and checks the allow/deny
decisions match what `access-policy.rego` should enforce.

```bash
python3 validate_opa_policy.py --host localhost --port 8181
```

## Recommended order

1. Bring up the full stack (phases 1-5)
2. Run `attack_simulation.py` against your lab target
3. Run `check_siem_ingestion.py` to confirm the alerts landed
4. Run `validate_opa_policy.py` to confirm the identity layer enforces access correctly
5. Screenshot the Kibana dashboard showing the alerts and drop it in the main README

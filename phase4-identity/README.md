# Phase 4: Identity and Zero Trust Access

## What this does
Implements identity-based access control using Keycloak as the identity provider and Open Policy Agent (OPA) as the policy engine making per-request authorization decisions based on user role and resource sensitivity.

## Components

### Keycloak (keycloak/)
- Runs on port 8081
- Admin credentials: admin / SASEforge@2025
- Configured for OAuth2 and TOTP-based MFA

### Open Policy Agent (opa-policies/access-policy.rego)
- Authenticated employees can access all resources except the restricted DB
- Admins can access everything including the restricted DB
- All unauthenticated requests are denied by default

## How to run
  cd keycloak
  docker compose up -d

Keycloak admin console at http://localhost:8081

## How to test OPA policy
  curl -X POST http://localhost:8181/v1/data/saseforge/authz/allow     -H "Content-Type: application/json"     -d '{"input": {"user": {"authenticated": true, "role": "employee"}, "resource": "restricted-db"}}'

Expected result: {"result": false} - employee denied DB access.

## Networking concepts demonstrated
- Zero trust architecture (never trust, always verify)
- Identity-aware access control
- OAuth2 token flow
- Attribute-based access control (ABAC)

# Phase 1: Network Foundation

## What this does
Creates three isolated Docker networks simulating enterprise network segmentation: a DMZ for public-facing services, an internal network for application servers, and a restricted network for the database layer.

## Network segments
- dmz-network: 10.0.1.0/24 - hosts the nginx web server exposed on port 8080
- internal-network: 10.0.2.0/24 - hosts the internal app server
- db-network: 10.0.3.0/24 - hosts the PostgreSQL database, no external exposure

## How to run
Run these commands in order:
  docker network create --subnet=10.0.1.0/24 dmz-network
  docker network create --subnet=10.0.2.0/24 internal-network
  docker network create --subnet=10.0.3.0/24 db-network
  docker compose up -d
  docker ps

## What to verify
- All three containers show as running in docker ps
- docker network ls shows all three networks
- DMZ web server responds at http://localhost:8080

## Networking concepts demonstrated
- Layer 3 network segmentation
- Subnet design for tiered security architecture
- Container isolation using bridge networks

# Phase 3: Proxy and CASB Layer

## What this does
Deploys Squid as a forward proxy intercepting all outbound HTTP/HTTPS traffic from the internal network. A block list of unauthorized cloud storage sites acts as a lightweight CASB layer enforcing which cloud applications users can access.

## Components

### Squid proxy (squid/squid.conf)
- Listens on port 3128
- Only allows traffic from internal network ranges
- Logs all requests to squid/logs/access.log

### CASB block list (squid/blocked-sites.txt)
Blocks: dropbox.com, wetransfer.com, pastebin.com, torrent.com, thepiratebay.org

## How to run
  cd squid
  docker compose up -d

## How to test
Set your browser proxy to localhost:3128, then visit dropbox.com.
You should see an access denied page from Squid.

## Networking concepts demonstrated
- Application layer (Layer 7) traffic inspection
- Forward proxy architecture
- Cloud application access control
- HTTP CONNECT tunneling for SSL traffic

#!/usr/bin/env bash
#
# dev-container.sh — one-command Home Assistant dev container startup.
#
# Personal convenience wrapper around the bare `devcontainers/cli`, needed
# because:
#   - IntelliJ's native Dev Container support currently fails on this
#     project's `features` (JetBrains bug IDEA-385013, unfixed as of writing)
#   - The bare CLI does not implement devcontainer.json's `forwardPorts`
#     (a documented limitation — only VS Code/JetBrains do that)
#
# This script builds/reuses the container, (re)creates a small socat sidecar
# to publish port 8123 to the host, then runs Home Assistant in the
# foreground. Ctrl+C stops Home Assistant; the container and port-forward
# stay up so the next run is fast. Not part of the project's shared tooling —
# safe to delete, and not needed if you use VS Code or a fixed IntelliJ.
#
# Usage:
#   ./dev-container.sh

set -euo pipefail

RED='\033[0;31m'
GREEN='\033[0;32m'
CYAN='\033[0;36m'
NC='\033[0m'

info() { echo -e "${CYAN}==> $1${NC}"; }
ok() { echo -e "${GREEN}✓ $1${NC}"; }
fail() {
    echo -e "${RED}✗ $1${NC}" >&2
    exit 1
}

command -v devcontainer >/dev/null 2>&1 || fail "devcontainer CLI not found. Install with: npm install -g @devcontainers/cli"

info "Checking Docker (Rancher Desktop)..."
docker info >/dev/null 2>&1 || fail "Cannot reach Docker. Is Rancher Desktop running?"
ok "Docker reachable"

info "Starting/reusing the dev container (fast if nothing changed)..."
UP_OUTPUT="$(devcontainer up --workspace-folder .)"
echo "$UP_OUTPUT"

CONTAINER_ID="$(echo "$UP_OUTPUT" | grep -oE '"containerId"\s*:\s*"[a-zA-Z0-9]+"' | tail -1 | cut -d'"' -f4)"
[[ -n "$CONTAINER_ID" ]] || fail "Could not determine the container ID from devcontainer up's output."
ok "Container ready: ${CONTAINER_ID:0:12}"

info "Setting up port forwarding (8123 -> host)..."
docker rm -f ha-port-forward >/dev/null 2>&1 || true
NET="$(docker inspect "$CONTAINER_ID" --format '{{range $k, $v := .NetworkSettings.Networks}}{{$k}}{{end}}')"
IP="$(docker inspect "$CONTAINER_ID" --format "{{(index .NetworkSettings.Networks \"$NET\").IPAddress}}")"
[[ -n "$NET" && -n "$IP" ]] || fail "Could not determine the container's network/IP."
docker run -d --name ha-port-forward --network "$NET" -p 8123:8123 \
    alpine/socat "tcp-listen:8123,fork,reuseaddr" "tcp-connect:$IP:8123" >/dev/null
ok "Port forward ready: http://localhost:8123 -> $IP:8123"

cleanup() {
    info "Stopping port forward (container keeps running for next time)..."
    docker rm -f ha-port-forward >/dev/null 2>&1 || true
}
trap cleanup EXIT INT TERM

echo ""
echo -e "${GREEN}Open http://localhost:8123 once Home Assistant finishes starting.${NC}"
echo -e "${CYAN}Press Ctrl+C here to stop Home Assistant.${NC}"
echo ""

devcontainer exec --workspace-folder . script/develop

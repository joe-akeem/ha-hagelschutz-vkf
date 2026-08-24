---
name: hagelschutz-devcontainer
description: >-
  Start, rebuild or troubleshoot the local Home Assistant dev container on this developer's machine
  (Rancher Desktop + IntelliJ IDEA, no working native Dev Container support). Use when asked to "start
  the devcontainer", "start Home Assistant locally", "test the integration locally", "run
  script/develop", or when the container fails to build, HA is unreachable at localhost:8123, or
  `hass`/`node`/`devcontainer` commands misbehave. Covers the one-command script, the IntelliJ
  dev-container bug and its CLI fallback, the Node/nvm version pitfall, and the manual port-forward fix
  the bare CLI needs since it lacks `forwardPorts`. SYMPTOMS — load this if about to: run
  `script/setup/bootstrap` or `script/develop` on the macOS host instead of the container; treat
  `docker ps` showing no port as proof the container is broken; combine `--network container:<id>` with
  `-p` in `docker run`; or chase a "randomUUID is not a function" crash as anything other than an old
  Node version.
---

# Start the local dev container

This machine cannot use IntelliJ's native Dev Container support for this project — it fails with
`Cannot get manifest for node feature` / `The server did not provide authentication method` while
resolving `ghcr.io/devcontainers/features/node`. That is [JetBrains bug
IDEA-385013](https://youtrack.jetbrains.com/issue/IDEA-385013), open since January 2026, alongside the
still-open feature request to fully support `devcontainer.json`'s `features` key
([IJPL-67123](https://youtrack.jetbrains.com/issue/IJPL-67123)). Re-test occasionally after an IntelliJ
update — if it starts working, IntelliJ handles port forwarding automatically and everything below
becomes unnecessary.

Until then, the fallback is the bare `@devcontainers/cli`, which works but does **not** implement
`forwardPorts` (a genuine, documented gap — only VS Code and JetBrains' native support do that), so port
8123 needs a manual publish step.

## Fast path

```bash
./dev-container.sh
```

Builds/reuses the container, (re)creates the port-forward, and runs `script/develop` in the foreground.
`Ctrl+C` stops Home Assistant; the container stays up for next time. This script is a personal
convenience wrapper (not shared project tooling) — see its header comment for what it automates.

## Manual step-by-step (when the script itself needs debugging)

1. **Docker reachable:** `docker info`. If not, start Rancher Desktop and wait for the whale/icon to
   settle. Its Docker socket is `~/.rd/docker.sock`, not Docker Desktop's default — if a tool insists on
   the Docker Desktop path, point it explicitly at Rancher Desktop's, and confirm **Preferences →
   Container Engine → "dockerd (moby)"** is selected (not `containerd`).
2. **Build/start the container:**

   ```bash
   devcontainer up --workspace-folder .
   ```

   Idempotent — reuses the existing container unless `devcontainer.json` changed. Only add
   `--remove-existing-container` to force a clean rebuild. The final line is JSON with the
   `containerId`; keep it, later steps need it.

3. **Confirm the venv actually exists** before assuming Home Assistant will start (see pitfall below):

   ```bash
   devcontainer exec --workspace-folder . bash -lc "ls -la .local/ha-venv/bin/hass"
   ```

   If missing, `postCreateCommand` did not finish — rerun it manually and watch for errors:
   `devcontainer exec --workspace-folder . bash .devcontainer/post-create.sh`.

4. **Start Home Assistant** (leave this terminal tab open):

   ```bash
   devcontainer exec --workspace-folder . script/develop
   ```

   Do not expect a "ready" banner at the end of the visible log — Home Assistant's HTTP server starts
   serving early, while slower integrations keep loading in the background. Confirm it directly instead
   of eyeballing the log:

   ```bash
   devcontainer exec --workspace-folder . curl -sS -o /dev/null -w '%{http_code}\n' --max-time 5 http://localhost:8123
   ```

   A `200`/`302` means it is already up, regardless of what the log's last line says.

5. **Publish port 8123 to the host** (replace `<id>` with the `containerId` from step 2):

   ```bash
   docker rm -f ha-port-forward 2>/dev/null
   NET=$(docker inspect <id> --format '{{range $k, $v := .NetworkSettings.Networks}}{{$k}}{{end}}')
   IP=$(docker inspect <id> --format "{{(index .NetworkSettings.Networks \"$NET\").IPAddress}}")
   docker run -d --name ha-port-forward --network "$NET" -p 8123:8123 \
     alpine/socat tcp-listen:8123,fork,reuseaddr tcp-connect:$IP:8123
   ```

   Open `http://localhost:8123`.

## Pitfalls already hit on this machine

- **`--network container:<id>` + `-p` in the same `docker run`: rejected.** Docker refuses this
  combination — joining another container's network namespace and publishing a port are mutually
  exclusive. Use a normal `--network <name>` attachment (step 5) instead.
- **The default `bridge` network has no name-based DNS.** `tcp-connect:<container-id>:8123` only
  resolves on a user-defined network. On `bridge` (`docker inspect` will say so), connect to the
  container's actual IP address instead, as step 5 does.
- **`TypeError: Pv.randomUUID is not a function` from `devcontainer`**: the active Node version predates
  `crypto.randomUUID` (needs 14.17+). Usually means a _different_ terminal tab is still on an old
  nvm-selected Node. Fix once, for every future shell: `nvm alias default v24.19.0` (swap in whatever
  `node --version` should resolve to), then open a new tab or `exec "$SHELL" -l"` to pick it up
  immediately. Quote glob-like arguments (`"lts/*"`) in zsh — unquoted, zsh treats them as a filename
  pattern and silently mangles the command.
- **`script/setup/bootstrap` fails with `local: -n: invalid option`** when run directly on the macOS
  host: that's Apple's stock `/bin/bash` 3.2 (`local -n` needs bash 4.3+). Home Assistant tooling is
  meant to run _inside_ the container, which has a current bash — run it via `devcontainer exec`, not on
  the host.
- **The venv lands at `.local/ha-venv` (workspace-relative), not `~/ha-venv`.** `resolve_venv_path()` in
  `script/.lib/output.sh` only prefers `$HOME/ha-venv` when `$REMOTE_CONTAINERS` or `$CODESPACES` is set
  — VS Code and Codespaces set that automatically, the bare CLI does not. Check the workspace-relative
  path first when the venv seems to be missing.
- **`hass: command not found` right after `devcontainer exec ... which hass`**: expected on a
  non-interactive/non-login shell — the venv activation lives in `~/.bashrc`, which `devcontainer exec`
  does not source by default. Use `bash -lc "..."` to force a login shell, or just run `script/develop`
  directly (it activates the venv itself via `activate_venv`, regardless of shell type).
- **`.git/hooks/pre-commit: line 13: exec: prek: not found` when committing from IntelliJ**: IntelliJ's
  commit action runs `git` on the **host**, not inside the container, so it never sees the container's
  venv where `prek` lives. This only happens because of the bare-CLI fallback above — VS Code's Dev
  Containers extension (and IntelliJ's native support, if the JetBrains bug ever gets fixed) runs Source
  Control operations _inside_ the container, where the hook works unmodified. Fix: `brew install prek` on
  the host (it is a standalone Rust binary, no container dependency) rather than patching the hook.
- **`ruff: command not found` / `yamllint: command not found` / etc. once `prek` itself runs on the
  host**: this project's hooks are configured against the container's preinstalled tools (`language:
system`), not prek's own isolated per-hook environments — installing `prek` alone is not enough.
  Installing every tool natively on the host duplicates the whole point of the devcontainer, so don't:
  either commit from inside the container (`devcontainer exec --workspace-folder . git commit -m "..."`
  — the actually-supported path) or, for a commit already validated via `script/lint`/`script/test` run
  some other way, skip the host-side hook for that one commit ("Commit without checks" in IntelliJ, or
  `git commit --no-verify`).

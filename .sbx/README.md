# Project sandbox

## One-time setup (per machine)

### 1. Install and sign in to `sbx`

```sh
brew install docker/tap/sbx
sbx login
```

See the [install guide](https://docs.docker.com/ai/sandboxes/install/) for
Windows/Linux instructions.

### 2. Register the Git MCP server

This runs local Git operations (log, diff, commit, branch, ...) on your
behalf, so Claude never needs a shell to use Git. Run this from your local
clone of the repo:

```sh
cd /path/to/your/clone/of/ha-hagelschutz-vkf
sbx mcp add git --command uvx --args mcp-server-git,--repository,"$(pwd)"
```

(Requires [`uv`](https://docs.astral.sh/uv/) to be installed, since the
server runs via `uvx`.)

### 3. Register the JetBrains MCP server

If you use an IntelliJ-based IDE (2025.2+), it has a built-in MCP server that
lets Claude drive IDE actions instead of shelling out. Enable it in
**Settings → Tools → MCP Server** and note the port shown there (e.g.
`64342`), then register it:

```sh
sbx mcp add jetbrains --url http://127.0.0.1:<PORT>/stream --skip-ssrf-check
```

`--skip-ssrf-check` is required and expected here: the server is on
`127.0.0.1`, which `sbx` normally blocks as a safety default for `--url`
registrations meant for remote endpoints. We're intentionally pointing at a
service on the same machine, so bypassing that check is correct.

Don't use IntelliJ? Skip this step and drop `jetbrains` from `--static-mcp`
below.

## Running the sandbox

```sh
cd /path/to/your/clone/of/ha-hagelschutz-vkf
sbx run claude --name hagelschutz --kit ./.sbx/kit --static-mcp git,jetbrains
```

- First run only: pick the **Balanced** network preset when prompted.
- First run only: run `/login` inside the Claude Code session to authenticate
  (OAuth browser flow). Credentials persist across later runs.
- `--static-mcp git,jetbrains` attaches exactly those two MCP servers and
  nothing else — Claude can't discover or attach other servers at runtime.

## Everyday commands

```sh
sbx stop hagelschutz            # stop the sandbox
sbx rm hagelschutz              # delete the sandbox
sbx mcp ls                      # list registered MCP servers
sbx exec -it hagelschutz bash   # YOUR shell into the sandbox VM, for debugging.
                                 # This is not available to Claude — Claude's
                                 # own Bash tool stays denied regardless.
```

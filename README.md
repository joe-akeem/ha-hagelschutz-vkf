# Hagelschutz VKF

[![GitHub Release][releases-shield]][releases]
[![GitHub Activity][commits-shield]][commits]
[![License][license-shield]](LICENSE)

[![hacs][hacsbadge]][hacs]
![Project Maintenance][maintenance-shield]

<!--
Uncomment and customize these badges if you want to use them:

[![BuyMeCoffee][buymecoffeebadge]][buymecoffee]
[![Discord][discord-shield]][discord]
-->

**✨ Develop in the cloud:** Want to contribute or customize this integration? Open it directly in GitHub Codespaces - no local setup required!

[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/joe-akeem/ha-hagelschutz-vkf?quickstart=1)

## ✨ Features

This integration polls the Swiss VKF "Hagelschutz einfach automatisch" hail-warning service
([meteo.netitservices.com](https://meteo.netitservices.com)) for the current hail-warning status of one registered
device/location, and exposes it as a single sensor so you can build your own automations on top of it — for example,
raising Somfy shutters when a hail warning starts.

- **Easy setup**: enter your device serial and hardware-type ID, no YAML required
- **Speaking state**: `no_hail` / `hail` / `test_alarm`, not a raw status code
- **Forward-compatible**: any field the API adds beyond `currentState` in the future shows up as an entity attribute
  instead of breaking the integration
- **Honest availability**: if the API can't be reached, the sensor goes `unavailable` — it never shows a stale value

**This integration will set up the following platform.**

| Platform | Description                                                    |
| -------- | -------------------------------------------------------------- |
| `sensor` | Current hail-warning status for the configured device/location |

> [!IMPORTANT]
> The vendor requires a **minimum poll interval of 120 seconds** — this integration polls at exactly that interval,
> and it is not configurable. Polling faster is not supported by the API.

## 🚀 Quick Start

### Step 1: Install the Integration

**Prerequisites:** This integration requires [HACS](https://hacs.xyz/) (Home Assistant Community Store) to be installed.

Click the button below to open the integration directly in HACS:

[![Open your Home Assistant instance and open a repository inside the Home Assistant Community Store.](https://my.home-assistant.io/badges/hacs_repository.svg)](https://my.home-assistant.io/redirect/hacs_repository/?owner=joe-akeem&repository=ha-hagelschutz-vkf&category=integration)

Then:

1. Click "Download" to install the integration
2. **Restart Home Assistant** (required after installation)

> [!NOTE]
> The My Home Assistant redirect will first take you to a landing page. Click the button there to open your Home Assistant instance.

<details>
<summary><strong>Manual Installation (Advanced)</strong></summary>

If you prefer not to use HACS:

1. Download the `custom_components/hagelschutz_vkf/` folder from this repository
2. Copy it to your Home Assistant's `custom_components/` directory
3. Restart Home Assistant

</details>

### Step 2: Add and Configure the Integration

**Important:** You must have installed the integration first (see Step 1) and restarted Home Assistant!

#### Option 1: One-Click Setup (Quick)

Click the button below to open the configuration dialog:

[![Open your Home Assistant instance and start setting up a new integration.](https://my.home-assistant.io/badges/config_flow_start.svg)](https://my.home-assistant.io/redirect/config_flow_start/?domain=hagelschutz_vkf)

Follow the setup wizard:

1. Enter your device serial (printed on the VKF hail sensor, e.g. `VKDEMO123456`)
2. Enter your hardware-type ID (given to you by the vendor)
3. Click Submit

The integration performs one test poll against the real API before creating the entry, so a wrong serial or
hardware-type ID is caught immediately instead of failing silently later.

#### Option 2: Manual Configuration

1. Go to **Settings** → **Devices & Services**
2. Click **"+ Add Integration"**
3. Search for "Hagelschutz VKF"
4. Follow the same setup steps as Option 1

### Step 3: Start Using!

The integration creates one sensor entity for the configured device:

- **Hail status**: `no_hail`, `hail`, or `test_alarm`, refreshed every 120 seconds

Find it in **Settings** → **Devices & Services** → **Hagelschutz VKF** → click on the device.

## Available Entities

### Sensor

- **Hail status**: the current hail-warning status
  - States: `no_hail` (0), `hail` (1), `test_alarm` (2)
  - Attributes: `raw_state` (the untranslated `currentState` value) plus any field the API returns beyond
    `currentState`

## Configuration

### During Setup

| Name             | Required | Description                                             |
| ---------------- | -------- | ------------------------------------------------------- |
| Device serial    | Yes      | The serial number printed on your VKF hail sensor       |
| Hardware type ID | Yes      | The hardware-type code for your device, from the vendor |

There are no options to adjust after setup — the poll interval is fixed at the vendor-mandated 120 seconds. Use
**Reconfigure** on the integration if your device serial or hardware-type ID changes.

## Troubleshooting

### Sensor shows "Unavailable"

The sensor goes `unavailable` whenever the last poll failed — this is deliberate, so you never automate off a stale
value. Check:

1. Your Home Assistant instance has internet access to `meteo.netitservices.com`
2. The device serial and hardware-type ID are still correct (use **Reconfigure** to update them)
3. The integration diagnostics (Settings → Devices & Services → Hagelschutz VKF → 3 dots → Download diagnostics)

### Enable Debug Logging

To enable debug logging for this integration, add the following to your `configuration.yaml`:

```yaml
logger:
  default: info
  logs:
    custom_components.hagelschutz_vkf: debug
```

## 🤝 Contributing

Contributions are welcome! Please open an issue or pull request if you have suggestions or improvements.

You have two options to set up a development environment — expand below for full details.

<details>
<summary><strong>Development Setup</strong></summary>

Both options provide the same fully-configured environment with Home Assistant, Python 3.14, Node.js LTS, and all necessary tools.

### Option 1: GitHub Codespaces (Recommended) ☁️

Develop directly in your browser without installing anything locally!

1. Click the green **"Code"** button in this repository
2. Switch to the **"Codespaces"** tab
3. Click **"Create codespace on main"**
4. **Wait for setup** (2-3 minutes first time) — everything installs automatically
5. **Review and commit** your changes in the Source Control panel (`Ctrl+Shift+G`)

> [!TIP]
> Codespaces gives you **60 hours/month free** for personal accounts. When you start Home Assistant (`script/develop`), port 8123 forwards automatically.

### Option 2: Local Development with VS Code 💻

#### Prerequisites

You'll need these installed locally:

- **A Docker-compatible container engine** — see options by platform:

  | Option                                                                                                                   | 🍎 macOS | 🐧 Linux | 🪟 Windows | Notes                                                                                                                                                                                                                                     |
  | ------------------------------------------------------------------------------------------------------------------------ | :------: | :------: | :--------: | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
  | [Docker Desktop](https://www.docker.com/products/docker-desktop/)                                                        |    ✅    |    ✅    |     ✅     | **Easiest starting point for all platforms.** GUI-based, well-documented, one installer. Uses WSL2 as default backend on Windows (Hyper-V also available). Installation requires admin rights; daily use does not. Free for personal use. |
  | [OrbStack](https://orbstack.dev/) ⭐                                                                                     |    ✅    |    —     |     —      | **Recommended for macOS** once Docker Desktop feels slow. Starts in ~2s, much lighter on RAM/CPU, full Docker API compatibility. Free for personal use.                                                                                   |
  | [Docker CE](https://docs.docker.com/engine/install/) (native) ⭐                                                         |    —     |    ✅    |     —      | **Recommended for Linux.** Install directly via your package manager — no VM, no GUI, no overhead. Free.                                                                                                                                  |
  | [WSL2](https://learn.microsoft.com/windows/wsl/install) + [Docker CE](https://docs.docker.com/engine/install/ubuntu/) ⭐ |    —     |    —     |     ✅     | **Recommended for Windows** once you're comfortable with WSL2. Docker runs natively inside WSL2 — no GUI overhead. Requires one-time WSL2 setup. Free.                                                                                    |
  | [Rancher Desktop](https://rancherdesktop.io/)                                                                            |    ✅    |    ✅    |     ✅     | Open source by SUSE. GUI-based, uses WSL2 on Windows. Good alternative to Docker Desktop. Free.                                                                                                                                           |
  | [Colima](https://github.com/abiosoft/colima)                                                                             |    ✅    |    ✅    |     —      | CLI-only, very lightweight. Good for terminal-focused workflows. Free.                                                                                                                                                                    |

- **VS Code** with the [Dev Containers extension](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers)
- **Git** — macOS and Linux usually have it already; see below if not, or to get a newer version:
  - **🍎 macOS:** The system Git (`xcode-select --install`) works fine. Recommended: `brew install git` ([Homebrew](https://brew.sh/)) for a current version.
  - **🐧 Linux:** Usually pre-installed. If not: `sudo apt install git` (or your distro's equivalent).
  - **🪟 Windows + WSL2 ⭐:** Install Git _inside WSL2_ with `sudo apt install git`. Git on Windows itself is not needed — VS Code clones and operates entirely within WSL2.
  - **🪟 Windows + Docker Desktop:** Install via `winget install Git.Git` or download [Git for Windows](https://git-scm.com/download/win).
- **Hardware** — the devcontainer runs a full Home Assistant instance including Python tooling:

  |          | Minimum    | Recommended                           |
  | -------- | ---------- | ------------------------------------- |
  | **RAM**  | 8 GB       | 16 GB or more                         |
  | **CPU**  | 4 cores    | 8 cores or more                       |
  | **Disk** | 10 GB free | 20 GB free (SSD strongly recommended) |

> [!TIP]
> **Not sure which Docker option to pick?** Start with [Docker Desktop](https://www.docker.com/products/docker-desktop/) — it works on all platforms, has a GUI, and needs no extra setup. The ⭐ options are faster alternatives once you're comfortable. macOS and Linux offer the best devcontainer experience — containers run with no extra VM layer and file I/O is fast. Windows works well too; this integration uses named container volumes (files live inside WSL2, not on the Windows drive) to keep performance acceptable.

> [!NOTE]
> **New to Dev Containers?** See the [VS Code Dev Containers documentation](https://code.visualstudio.com/docs/devcontainers/containers#_system-requirements) for system requirements and how to install the extension. **Once the extension is installed, you're done** — this repository already ships a complete devcontainer configuration. You don't need to follow the rest of the VS Code guide; the setup steps below are all that's needed.

#### Setup Steps

1. **Clone in a Dev Container:**

   **🍎 macOS / 🐧 Linux:** Clone the repository and open the folder in VS Code → click **"Reopen in Container"** when prompted (or `F1` → **"Dev Containers: Reopen in Container"**).

   **🪟 Windows:** In VS Code, press `F1` → **"Dev Containers: Clone Repository in Named Container Volume..."** and enter the repository URL. This keeps files inside WSL2 for best I/O performance.

2. Wait for the container to build (2-3 minutes first time)

3. **Review and commit** changes in Source Control (`Ctrl+Shift+G`)

4. **Start developing**:

   ```bash
   script/develop  # Home Assistant runs at http://localhost:8123
   ```

> [!NOTE]
> Both Codespaces and local DevContainer provide the exact same experience. The only difference is where the container runs (GitHub's cloud vs. your machine).

</details>

---

## 🤖 AI-Assisted Development

> [!NOTE]
> **Transparency Notice:** This integration was developed with assistance from AI coding agents (GitHub Copilot,
> Claude, and others). AI assistance by itself neither guarantees nor rules out software quality. To make an informed
> installation decision, review the project's stated maturity, known limitations, automated test coverage, real-device
> testing, and the extent of human review. The maintainer should replace the fields below with accurate project-specific
> details rather than implying checks that were not performed. See the blueprint's [`AI_POLICY.md`](AI_POLICY.md) for
> guidance.
>
> - **AI assistance:** substantial
> - **Human review:** partial
> - **Automated tests:** config flow, coordinator state mapping, entity availability, diagnostics redaction — see `tests/`
> - **Real-device or service testing:** not yet performed as of this integration's initial scaffolding
> - **Maturity and known limitations:** early / pre-1.0; only tested against the documented API contract, not yet
>   against a live device
>
> If you encounter unexpected behavior, please [open an issue](../../issues) on GitHub.

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

**Made with ❤️ by [@joe-akeem][user_profile]**

---

[commits-shield]: https://img.shields.io/github/commit-activity/y/joe-akeem/ha-hagelschutz-vkf.svg?style=for-the-badge
[commits]: https://github.com/joe-akeem/ha-hagelschutz-vkf/commits/main
[hacs]: https://github.com/hacs/integration
[hacsbadge]: https://img.shields.io/badge/HACS-Default-orange.svg?style=for-the-badge
[license-shield]: https://img.shields.io/github/license/joe-akeem/ha-hagelschutz-vkf.svg?style=for-the-badge
[maintenance-shield]: https://img.shields.io/badge/maintainer-%40joe-akeem-blue.svg?style=for-the-badge
[releases-shield]: https://img.shields.io/github/release/joe-akeem/ha-hagelschutz-vkf.svg?style=for-the-badge
[releases]: https://github.com/joe-akeem/ha-hagelschutz-vkf/releases
[user_profile]: https://github.com/joe-akeem

<!-- Optional badge definitions - uncomment if needed:
[buymecoffee]: https://www.buymeacoffee.com/jpawlowski
[buymecoffeebadge]: https://img.shields.io/badge/buy%20me%20a%20coffee-donate-yellow.svg?style=for-the-badge
[discord]: https://discord.gg/Qa5fW2R
[discord-shield]: https://img.shields.io/discord/330944238910963714.svg?style=for-the-badge
-->

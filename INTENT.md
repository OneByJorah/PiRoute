# INTENT.md — J1-PIPELINE Phase -1 (ORACLE)

**Repository:** `OneByJorah/PiRoute`
**Analysis Date:** 2026-07-05
**Analyst:** J1-PIPELINE ORACLE (read-only)
**Status:** Intent Reconstructed

---

## What This System Does

**PiRouter Pro** is a Flask-based web dashboard and management platform for Raspberry Pi-based edge routers. It provides a single-pane-of-glass interface for monitoring and controlling a Linux router's core functions.

### Services & Capabilities

| Capability | Implementation | Details |
|---|---|---|
| **Real-Time Monitoring** | `psutil` + `vcgencmd` | CPU %, memory %, disk usage, temperature, uptime, external IP |
| **Traffic Analytics** | SQLite time-series DB | 60-second background sampling; 24h/3d/7d bucketed views (15min/1h/2h buckets) |
| **Client Tracking** | `dnsmasq.leases` parsing | MAC, IP, hostname, lease expiry for all connected LAN clients |
| **VPN Management** | Shell commands via `subprocess` | Start/stop/status for WireGuard, Tailscale, Cloudflare WARP, NordVPN, NetBird, UniFi Teleport |
| **Tailscale Exit Nodes** | `tailscale exit-node list` | List and select exit nodes; auto-best-exit via external script |
| **Speed Testing** | `speedtest-cli` | On-demand download/upload bandwidth tests |
| **System Logs** | `tail -n 200` on log files | View last 50 lines of syslog, WARP, WireGuard, Tailscale, NordVPN, NetBird logs |
| **System Controls** | `subprocess` + `sudo` | Reboot, VPN service start/stop |

### Operational Role

The system runs as a long-lived daemon on a Raspberry Pi configured as a network router. It serves a dark-themed web dashboard on `http://127.0.0.1:5000` (localhost-only by default) that an administrator accesses via browser. A background thread collects system metrics every 60 seconds and stores them in SQLite at `/var/lib/pirouter/traffic.db`. The frontend polls `/api/stats` every 10 seconds for live updates.

---

## Why This Was Built

### Real Problem

Managing a Raspberry Pi-based edge router requires SSH access and manual command-line operations for every task — checking system load, seeing who's connected, toggling VPNs, viewing logs, running speed tests. There was no unified, real-time, browser-accessible dashboard that consolidated all these functions into one place with historical data.

The original code (initial commit `71d6775`, 2026-05-15) was uploaded as a bulk set of files — a working but incomplete Flask app with a 1241-line HTML dashboard. It was missing critical pieces: the `/api/logs` endpoint the frontend referenced, the correct template folder path, startup scripts, a systemd service, and proper documentation. The FIXES.md documents that these were all added in a single fix commit (`50d50f3`, 2026-06-14).

### Why Existing Tools Were Insufficient

- **SSH + CLI tools** (`htop`, `iftop`, `wg show`, `journalctl`): Powerful but require terminal access, no history, no unified view, no visual dashboard.
- **Netdata / Grafana + Prometheus**: Overkill for a single Raspberry Pi router; require significant setup, resource overhead, and separate metric collection infrastructure.
- **Router vendor UIs** (OpenWRT, pfSense, OPNsense): Not available on a standard Raspberry Pi OS install; require flashing a custom firmware.
- **Commercial router dashboards**: Proprietary, expensive, not designed for DIY Raspberry Pi routers.
- **Existing Flask dashboards**: None found that combined all of: real-time system stats, VPN management across 6 providers, dnsmasq client tracking, speed testing, log viewing, and historical traffic bucketing in a single lightweight app.

### What Triggered Development

The JorahOne infrastructure runs on Raspberry Pi edge routers at various locations. The need for a lightweight, self-contained, browser-accessible management interface that could run on a stock Raspberry Pi OS without Docker or additional infrastructure drove the creation of this tool. The repo was originally created under a different name and later renamed to **PiRoute** (as seen in the git history: `4e6eeae` through `d7a6335` all deal with renaming references).

The repo has since been standardized through the J1 pipeline: ruff auto-fixes, J1 brand-standard README, dependabot, CodeQL CI/CD, community governance files, and a security audit (`b37569a`).

### Ecosystem Fit

```
JorahOne LLC / OneByJorah Organization
│
├── PiRoute (PiRouter Pro)    ← YOU ARE HERE
│   └── Raspberry Pi edge router management dashboard
│
├── Other J1 repos               (infrastructure, security, monitoring, agents)
│
└── J1-PIPELINE                  (lifecycle management for all repos)
```

PiRoute fills the **edge device management** niche in the JorahOne ecosystem — providing operational visibility and control for the physical Raspberry Pi routers that connect JorahOne services to the internet.

---

## Operational Classification

**Classification: BETA → PRODUCTION (transitioning)**

### Evidence for Production Readiness

| Evidence | Source |
|---|---|
| v1.0.0 tagged | `CHANGELOG.md` — "Initial release" dated 2026-07-04 |
| systemd service file | `systemd/pirouter.service` — auto-restart, journal logging |
| CodeQL CI/CD | `.github/workflows/codeql.yml` — push/PR/schedule scans for Python + JS/TS |
| Dependabot configured | `.github/dependabot.yml` — weekly pip + npm + docker + GitHub Actions updates |
| Security policy | `SECURITY.md` — 48h acknowledgment, 90-day disclosure timeline |
| Code of Conduct | `CODE_OF_CONDUCT.md` — Contributor Covenant v2.1 |
| Contributing guide | `CONTRIBUTING.md` — PR workflow, style guides, issue labels |
| Issue/PR templates | `.github/ISSUE_TEMPLATE/` (bug + feature) + `PULL_REQUEST_TEMPLATE.md` |
| Security audit in history | `b37569a` — "audit(PiRoute): sanitize email and path references" |
| MIT License | `LICENSE` — standard open-source |
| Background metric sampling | `app.py` — 60-second daemon thread for time-series data |
| Production deployment docs | `FIXES.md` — systemd enable/start, journalctl monitoring |

### Evidence of Beta / Gaps

| Gap | Source | Impact |
|---|---|---|
| **No tests** | No `test_*.py`, no test directory | No regression safety net |
| **No Docker support** | No `Dockerfile` or `docker-compose.yml` | Deployment tied to bare-metal Pi OS |
| **Demo/fallback code in frontend** | `template/dashboard.html` line 1230: `tryDemo()` seeds fake data when API unreachable | Development artifact in production code |
| **systemd path mismatch** | `pirouter.service` uses `WorkingDirectory=/var/www/pirouter-pro` but repo lives elsewhere | Deployment documentation gap |
| **Dependabot ecosystem mismatch** | Configured for `npm` and `docker` but no `package.json` or `Dockerfile` exists | Template vestige |
| **No static directory** | `app.py` sets `static_folder="static"` but no `static/` dir exists | Flask will 404 on static files |
| **No Docker compose** | No containerization at all | Single-machine deployment only |
| **No health check endpoint** | No `/health` or `/readyz` endpoint | No liveness/readiness for orchestration |

---

## Key Architectural Decisions

1. **Flask + SQLite (no ORM)** — Minimal dependencies, zero configuration, runs on stock Raspberry Pi OS. SQLite is sufficient for single-node time-series data at 60-second granularity.

2. **Shell commands via `subprocess` for all system interactions** — Avoids Python-native libraries for VPN/service management. Simple but fragile: depends on exact CLI output formats and `sudo` access.

3. **Background daemon thread for metric collection** — Non-blocking 60-second sampling loop. Silently swallows exceptions (bare `except: pass`), which means failures are invisible to the operator.

4. **Localhost-only binding** — `app.run(host="127.0.0.1")` by default. Security-conscious: the dashboard is not exposed to the network without explicit firewall configuration.

5. **Single monolithic HTML file** — 1241-line dashboard with inline CSS and JS. No build step, no framework, no bundler. Fast to deploy, hard to maintain at scale.

6. **Bucketed time-series with delta computation** — Traffic history is stored as cumulative counters and bucketed client-side into 15min/1h/2h windows with delta calculations between consecutive buckets. Avoids storing per-second data.

7. **VPN abstraction via dict-based service registry** — `VPN_SERVICES` dict maps service keys to check/start/stop commands. Adding a new VPN provider is a one-line config change.

---

## Repository Structure

```
PiRoute/
├── app.py                          # Flask web server + background collector (290 lines)
├── init_db.py                      # Database initialization script (32 lines)
├── start.sh                        # Startup script (20 lines)
├── requirements.txt                # Dependencies: flask, psutil, speedtest-cli
├── CHANGELOG.md                    # v1.0.0 — 2026-07-04
├── FIXES.md                        # Fixes and deployment guide (157 lines)
├── ROADMAP.md                      # Production stability, docs, test coverage
├── README.md                       # J1 brand-standard README
├── LICENSE                         # MIT
├── .gitignore                      # Python + IDE + OS + env + logs
│
├── template/
│   └── dashboard.html              # Single-page dashboard (1241 lines, 51KB)
│
├── systemd/
│   └── pirouter.service            # systemd unit file
│
├── docs/
│   └── screenshots/
│       └── pirouter-dashboard.png
│
├── .github/
│   ├── dependabot.yml              # pip + npm + docker + actions (weekly)
│   ├── workflows/
│   │   └── codeql.yml              # CodeQL analysis (Python + JS/TS)
│   └── ISSUE_TEMPLATE/
│       ├── bug_report.md
│       ├── feature_request.md
│       └── PULL_REQUEST_TEMPLATE.md
│
├── CODE_OF_CONDUCT.md
├── CONTRIBUTING.md
├── SECURITY.md
└── INTENT.md                       ← THIS FILE (Phase -1 output)
```

---

## Notes

### Naming Discrepancy
The repo is named **PiRoute** but the project is branded as **PiRouter Pro** throughout the code (app title, README, systemd service description, FIXES.md). The git history shows a rename from the original name to PiRoute (commits `4e6eeae` → `d7a6335`), but the internal branding was never updated to match.

### Config Drift Findings
- **Dependabot ecosystem mismatch**: Configured for `npm` and `docker` ecosystems despite no `package.json` or `Dockerfile` existing. Template vestige from J1 repo template.
- **systemd path mismatch**: `pirouter.service` specifies `WorkingDirectory=/var/www/pirouter-pro` and `ExecStart=/usr/bin/python3 /var/www/pirouter-pro/app.py`, but the repo is cloned elsewhere. The `start.sh` script uses the correct local path. This is a deployment documentation gap.
- **Demo/fallback code in production frontend**: `tryDemo()` at line 1230 of `dashboard.html` seeds fake data when the API is unreachable. Useful for development but should be removed for production.
- **Missing `static/` directory**: `app.py` configures `static_folder="static"` but no `static/` directory exists in the repo. The dashboard has no static assets to serve (CSS/JS are inline), so this is harmless but misleading.

### Security Audit
Commit `b37569a` ("audit(PiRoute): sanitize email and path references") is the most recent commit and represents a security sanitization pass. This is a positive maturity signal.

### No Tests
The repo has zero test files. No unit tests, integration tests, or smoke tests exist. This is the most significant quality gap for a production-classified system.

### No Docker Support
The system is designed for bare-metal Raspberry Pi OS deployment only. No containerization exists, which limits deployment flexibility and reproducibility.

### Initial Commit
The initial commit (`71d6775`, 2026-05-15) was a bulk upload of 5 files (LICENSE, README.md, app.py, requirements.txt, template/dashboard.html) — 1562 lines of code. This was the "first thing" the author considered the complete initial version, though it was missing several critical pieces that were added a month later in commit `50d50f3`.

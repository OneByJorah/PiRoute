<!-- j1-brand:v2 -->
<div align="center">

# EdgeRouter (PiRouter Pro)

A professional Raspberry Pi router dashboard and backend management platform — real-time traffic monitoring, VPN status, client lease tracking, and system controls.

[![GitHub](https://img.shields.io/badge/github-OneByJorah%2FEdgeRouter-FFB300?style=for-the-badge&labelColor=0d0d0c)](https://github.com/OneByJorah/EdgeRouter)
[![License](https://img.shields.io/badge/license-MIT-FFB300?style=for-the-badge&labelColor=0d0d0c)](LICENSE)
[![Language](https://img.shields.io/badge/HTML-FFB300?style=for-the-badge&labelColor=0d0d0c)](https://developer.mozilla.org/en-US/docs/Web/HTML)
[![Built by](https://img.shields.io/badge/built%20by-JorahOne%20LLC-FFB300?style=for-the-badge&labelColor=0d0d0c)](https://github.com/OneByJorah)

</div>

---

## Why This Exists

Managing a Raspberry Pi that acts as a router means juggling SSH sessions, config files, and command-line tools. EdgeRouter (PiRouter Pro) gives you a web dashboard for the whole thing — live traffic graphs, VPN health (WireGuard, Tailscale), dnsmasq client leases, on-demand speed tests, and system reboot — all backed by a time-series SQLite database.

## Key Features

| Feature | Why It Matters |
|---|---|
| Live traffic monitoring | Real-time bandwidth and connection tracking |
| VPN status dashboard | WireGuard and Tailscale health at a glance |
| Client lease tracking | See which devices are on your network via dnsmasq |
| On-demand speed tests | Test throughput without leaving the dashboard |
| Service management | Start, stop, and restart services from the UI |
| REST API | `/api/stats`, `/api/traffic`, and more for external integration |

## Quick Start

```bash
git clone https://github.com/OneByJorah/EdgeRouter.git
cd EdgeRouter
pip install -r requirements.txt
sudo python3 app.py   # requires root for system service management
```

The dashboard is available at `http://<raspberry-pi-ip>:5000`.

## Architecture

```
┌──────────┐     ┌──────────────┐     ┌──────────────┐
│  Network   │────▶│  EdgeRouter   │────▶│  SQLite       │
│  Services  │     │  Flask App    │     │  Time-Series  │
│  dnsmasq   │     │  (Port 5000)  │     │               │
│  WireGuard │     │  Jinja2 UI    │     │               │
│  Tailscale │     │  REST API     │     │               │
└──────────┘     └──────────────┘     └──────────────┘
```

## Documentation

| Doc | Description |
|---|---|
| [Setup Guide](docs/setup.md) | Installing and configuring EdgeRouter |
| [API Reference](docs/api.md) | REST endpoint documentation |
| [Dashboard Guide](docs/dashboard.md) | Using the web interface |

---

## License

MIT © JorahOne, LLC — see [LICENSE](LICENSE)

<sub>Part of the JorahOne infrastructure ecosystem.</sub>

# PiRoute

Professional Raspberry Pi router dashboard — transform your Pi into a network router with web-based management.

![status](https://img.shields.io/badge/status-active-FFB300?style=flat-square)
![language](https://img.shields.io/badge/python-3.10+-0d0d0c?style=flat-square)
![license](https://img.shields.io/badge/license-MIT-FFB300?style=flat-square)

## Overview

PiRoute is a self-hosted Raspberry Pi router dashboard and management platform. It provides a modern web interface for managing network routing, firewall rules, port forwarding, DHCP, DNS, and VPN on a Raspberry Pi. Features real-time traffic monitoring, device discovery, and Docker deployment.

## Features

- Real-time dashboard with live network statistics
- Visual network map of connected devices
- Traffic monitoring with bandwidth usage charts
- Firewall rule management (iptables/nftables)
- Port forwarding configuration
- Built-in DHCP and DNS server management (dnsmasq)
- VPN support (WireGuard, OpenVPN)
- Docker Compose deployment

## Architecture / Tech Stack

- **Backend**: Flask (Python 3.10+)
- **Database**: SQLite
- **Network**: iptables/nftables, dnsmasq, hostapd
- **VPN**: WireGuard, OpenVPN
- **Deployment**: Docker Compose, systemd

## Installation

```bash
git clone https://github.com/OneByJorah/PiRoute.git
cd PiRoute

# Docker (recommended)
docker compose up -d

# Or direct install
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python app.py
```

Open `http://raspberrypi:5000` (default: `admin` / `admin`).

## Configuration

| Variable | Default | Description |
|----------|---------|-------------|
| `PIROUTE_PORT` | `5000` | Dashboard port |
| `PIROUTE_HOST` | `0.0.0.0` | Bind address |
| `NETWORK_INTERFACE` | `eth0` | Primary network interface |
| `WIFI_INTERFACE` | `wlan0` | WiFi interface |

## License

MIT — see [LICENSE](LICENSE).

---
Part of the JorahOne / J1 ecosystem — Raspberry Pi network routing and management.

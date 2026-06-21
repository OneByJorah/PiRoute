# EdgeRouter — PiRouter Pro

**Version:** v1.0  
**Status:** Active Development  
**Repository:** https://github.com/OneByJorah/EdgeRouter

---

## Table of Contents

- [Overview](#overview)
- [Architecture](#architecture)
- [Technology Stack](#technology-stack)
- [Features](#features)
- [Getting Started](#getting-started)
- [Service Management](#service-management)
- [Project Structure](#project-structure)
- [Screenshots](#screenshots)
- [Contributing](#contributing)
- [License](#license)
- [Author](#author)

---

## Overview

PiRouter Pro is a Flask-based router monitoring and management dashboard for Linux edge devices (Raspberry Pi and similar hosts). It provides real-time traffic, CPU, memory, temperature, VPN status, and connected-client metrics via a responsive web UI backed by SQLite.

Built for self-hosted edge deployments where visibility into network health matters.

---

## Architecture

Browser → Flask backend (`app.py`, port `5000`) → SQLite (`/var/lib/pirouter/traffic.db`) → system metrics (psutil, speedtest-cli) → dashboard templates.

A background thread records traffic snapshots every minute. Systemd is used for production service management.

---

## Technology Stack

| Layer | Stack |
|---|---|
| Runtime | Linux (Ubuntu 22.04+, Raspberry Pi OS) |
| Backend | Python / Flask |
| Database | SQLite (`/var/lib/pirouter/traffic.db`) |
| Metrics | psutil, speedtest-cli |
| Frontend | HTML5 Dashboard (template/dashboard.html) |
| Process Manager | systemd (`systemd/pirouter.service`) |
| VCS | Git + GitHub (`github.com/OneByJorah/EdgeRouter`) |

---

## Features

- **Traffic monitoring**: RX/TX bytes, client counts, CPU, memory, temperature.
- **VPN status**: tracked in the traffic history.
- **Speedtest integration**: on-demand bandwidth checks.
- **Persistent history**: SQLite-backed time-series metrics.
- **Systemd managed**: production-ready service unit included.
- **Edge-optimized**: lightweight enough for Raspberry Pi class hardware.

---

## Getting Started

```bash
# 1. Clone the repository
git clone https://github.com/OneByJorah/EdgeRouter.git
cd EdgeRouter

# 2. Create virtual environment
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# 3. Initialize data directory (run as root for DB path)
sudo ./init_db.py

# 4. Start the dashboard
sudo ./start.sh
# Or run directly:
# sudo python3 app.py
```

Visit `http://localhost:5000`.

---

## Service Management

```bash
# Install systemd unit (copy to /etc/systemd/system/)
sudo cp systemd/pirouter.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable --now pirouter.service

# Tail logs
sudo journalctl -u pirouter.service -f
```

---

## Project Structure

```
EdgeRouter/
├── app.py                 # Flask backend + routes
├── init_db.py             # SQLite bootstrap
├── start.sh               # Root startup wrapper
├── requirements.txt       # Python deps
├── systemd/
│   └── pirouter.service   # systemd unit
├── template/
│   └── dashboard.html     # Dashboard UI
├── static/                # CSS/JS assets
└── docs/screenshots/
    └── edgerouter-dashboard.png
```

---

## Screenshots

All screenshots are live captures from the local PiRouter Pro instance.

### Dashboard
![PiRouter Pro Dashboard](docs/screenshots/edgerouter-dashboard.png)

---

## Contributing

1. Create a feature branch off `main`.
2. Test on a Raspberry Pi or compatible Linux device.
3. Submit a PR with description and screenshots for UI changes.

---

## License

MIT

---

## Author

Built by **Jhonattan L. Jimenez**.

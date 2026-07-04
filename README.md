# EdgeRouter — PiRouter Pro

**Flask-based router monitoring and management dashboard for Linux edge devices.**

![License](https://img.shields.io/badge/License-MIT-FFB300.svg?style=for-the-badge)
![Status](https://img.shields.io/badge/Status-Active_Development-FFB300.svg?style=for-the-badge)
![Language](https://img.shields.io/badge/Language-Python-FFB300.svg?style=for-the-badge)
![Stack](https://img.shields.io/badge/Stack-Flask_SQLite_psutil-FFB300.svg?style=for-the-badge)
![Platform](https://img.shields.io/badge/Platform-Linux-FFB300.svg?style=for-the-badge)

EdgeRouter monitors and manages Linux edge devices through a responsive Flask web UI backed by SQLite. It captures real-time traffic, CPU, memory, temperature, VPN status, and connected-client metrics. Built for Raspberry Pi and compatible hosts, it provides persistent time-series history via a lightweight systemd-managed service.

- Persistent SQLite-backed metrics history.
- Background traffic snapshots recorded every minute.
- Systemd unit for production lifecycle management.
- Local-only interface with no cloud dependencies.

- Start the dashboard with `sudo ./start.sh`.
- Initialize the SQLite database with `sudo ./init_db.py`.
- Install the systemd service with `systemctl enable --now pirouter.service`.
- View live traffic, CPU, memory, and temperature from the web UI.
- Capture on-demand bandwidth checks via speedtest-cli.

```
Browser → Flask backend (5000) → SQLite (/var/lib/pirouter/traffic.db)
                                   ├── psutil (system metrics)
                                   └── speedtest-cli (bandwidth)
Background thread → records traffic snapshots every 60s
```

### Technology Stack

- **Runtime**: Linux (Ubuntu 22.04+, Raspberry Pi OS)
- **Backend**: Python / Flask
- **Database**: SQLite
- **Metrics**: psutil, speedtest-cli
- **Frontend**: HTML5 Dashboard
- **Process Manager**: systemd
- **VCS**: Git + GitHub

### Quickstart

1. Clone the repository.
   ```bash
   git clone https://github.com/OneByJorah/EdgeRouter.git
   cd EdgeRouter
   ```
2. Create a virtual environment and install dependencies.
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```
3. Initialize the data directory.
   ```bash
   sudo ./init_db.py
   ```
4. Start the dashboard.
   ```bash
   sudo ./start.sh
   ```
5. Verify the UI at `http://localhost:5000`.

### Roadmap

- [ ] Add SNMP polling module
- [ ] Export metrics to Prometheus pushgateway
- [ ] Add alerting rules for threshold breaches
- [ ] Provide Docker image for containerized deployment

### License

MIT © JorahOne, LLC

---

*Built by [JorahOne, LLC](https://github.com/JorahOne-Services) — network security, AD/M365, and infrastructure automation for SMBs and public sector.*

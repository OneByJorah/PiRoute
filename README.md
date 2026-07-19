<div align="center">

  # 🍓 PiRoute Pro

  **Professional Raspberry Pi Router Dashboard & Management Platform**

  Transform your Raspberry Pi into a powerful network router with a modern web-based management interface

  [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
  [![Python 3.10+](https://img.shields.io/badge/Python-3.10+-3776AB?style=flat&logo=python&logoColor=white)](https://www.python.org/)
  [![Flask](https://img.shields.io/badge/Flask-000000?style=flat&logo=flask&logoColor=white)](https://flask.palletsprojects.com/)
  [![Raspberry Pi](https://img.shields.io/badge/Raspberry%20Pi-A51931?style=flat&logo=raspberrypi&logoColor=white)](https://www.raspberrypi.org/)
  [![Docker](https://img.shields.io/badge/Docker-2496ED?style=flat&logo=docker&logoColor=white)](https://www.docker.com/)

  [Features](#-features) • [Quick Start](#-quick-start) • [Architecture](#-architecture) • [API](#-api-reference) • [Contributing](#-contributing)

</div>

---

## 📸 Screenshots

<div align="center">

![Dashboard](docs/screenshots/dashboard.png)

*Live router dashboard — captured from the running Flask app (real CPU/disk/net stats).*

</div>

> 💡 **Tip:** PiRoute Pro provides real-time network monitoring with beautiful visualizations

---

## ✨ Features

| Feature | Description |
|---------|-------------|
| 📊 **Real-Time Dashboard** | Live network statistics and performance metrics |
| 🗺️ **Network Map** | Visual topology of connected devices |
| 📈 **Traffic Monitoring** | Bandwidth usage per device and application |
| 🔥 **Firewall Management** | iptables/nftables rule management |
| 🔌 **Port Forwarding** | Easy port forwarding configuration |
| 📱 **DHCP Server** | Built-in DHCP server management |
| 🌐 **DNS Server** | Local DNS resolution with ad-blocking |
| 🔐 **VPN Support** | WireGuard/OpenVPN integration |
| 🐳 **Docker Ready** | Easy deployment on Raspberry Pi |

---

## 🚀 Quick Start

### Prerequisites

- Raspberry Pi 4/5 (4GB+ RAM recommended)
- Raspberry Pi OS (64-bit) or Ubuntu Server
- Docker & Docker Compose
- Two network interfaces (Ethernet + WiFi recommended)

### Installation

#### Option 1: Docker (Recommended)

```bash
# Clone the repository
git clone https://github.com/OneByJorah/PiRoute.git
cd PiRoute

# Start with Docker
docker compose up -d
```

#### Option 2: Direct Installation

```bash
# Clone the repository
git clone https://github.com/OneByJorah/PiRoute.git
cd PiRoute

# Install dependencies
pip install -r requirements.txt

# Start the dashboard
python app.py
```

### Access the Dashboard

Open **http://localhost:5000** in your browser.

> The app binds to `127.0.0.1:5000` and must run as root (it writes to `/var/lib/pirouter/traffic.db` and calls `iptables`/`wg`/etc.). On a Pi: `sudo python3 app.py`. There is **no built-in authentication** — put it behind a reverse proxy if exposed.

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                      PiRoute Pro                            │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│   ┌──────────┐      ┌──────────┐      ┌──────────────┐    │
│   │ Browser  │ ───▶ │  Nginx   │ ───▶ │ Flask Backend │    │
│   └──────────┘      └──────────┘      └──────┬───────┘    │
│                                               │             │
│                                   ┌───────────┴──────────┐ │
│                                   │                      │ │
│                        ┌──────────┴──────────┐           │ │
│                        │                     │           │ │
│                        ▼                     ▼           │ │
│                 ┌──────────┐          ┌──────────┐      │ │
│                 │ Network  │          │   SQLite │      │ │
│                 │ Manager  │          │   Data   │      │ │
│                 │(iptables)│          │          │      │ │
│                 └──────────┘          └──────────┘      │ │
│                                                           │ │
│  ┌─────────────────────────────────────────────────────┐ │ │
│  │              Network Services                       │ │ │
│  │  ┌─────────┐  ┌─────────┐  ┌─────────┐            │ │ │
│  │  │  DHCP   │  │   DNS   │  │   VPN   │            │ │ │
│  │  │ Server  │  │ Server  │  │ Gateway │            │ │ │
│  │  └─────────┘  └─────────┘  └─────────┘            │ │ │
│  └─────────────────────────────────────────────────────┘ │
│                                                           │
└─────────────────────────────────────────────────────────────┘
```

### Tech Stack

| Component | Technology |
|-----------|------------|
| **Backend** | Python 3.10+, Flask |
| **Frontend** | HTML5, CSS3, JavaScript, Chart.js |
| **Database** | SQLite |
| **Network** | iptables/nftables, dnsmasq, hostapd |
| **VPN** | WireGuard, OpenVPN |
| **Deployment** | Docker / Direct install |

---

## 📁 Project Structure

```
PiRoute/
├── app.py                  # Flask app (all routes) + background traffic recorder
├── template/
│   └── dashboard.html      # Jinja2 dashboard template
├── static/                 # CSS, JS, images (if present)
├── init_db.py              # DB init helper
├── docker-compose.yml      # Docker deployment
├── Dockerfile              # python:3.x-slim, runs as root
├── requirements.txt        # flask, psutil, speedtest-cli
└── docs/screenshots/       # captured from the running server
```

---

## 🔌 API Reference

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | `GET` | Main dashboard |
| `/api/stats` | `GET` | System + VPN status (CPU, mem, disk, net, ext IP, VPN list) |
| `/api/traffic` | `GET` | Historical traffic rows from SQLite (`?period=24h`) |
| `/api/clients` | `GET` | Connected clients |
| `/api/vpn/<action>/<service>` | `POST` | Start/stop a VPN service (WireGuard, WARP, Mesh-VPN, NordVPN, NetBird) |
| `/api/mesh-vpn/exit-nodes` | `GET` | Mesh-VPN exit-node list |
| `/api/mesh-vpn/set-exit` | `POST` | Set Mesh-VPN exit node |
| `/api/speedtest` | `GET` | Run a speedtest (needs `speedtest-cli`) |
| `/api/reboot` | `POST` | Reboot the host (requires root) |
| `/api/logs` | GET/POST | Read/post service logs |

### Example Usage

```bash
# Live stats
curl http://localhost:5000/api/stats

# Traffic history
curl http://localhost:5000/api/traffic?period=24h
```

---

## 🛠️ Development

### Local Development

```bash
git clone https://github.com/OneByJorah/PiRoute.git
cd PiRoute
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
sudo python app.py        # binds 127.0.0.1:5000
```

> There is no test suite yet. Verify by loading the dashboard and the `/api/*` endpoints.

---

## 🤝 Contributing

Contributions are welcome! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🔒 Security

For security concerns, please see [SECURITY.md](SECURITY.md).

---

## 💬 Support

- 📧 Email: support@jorah.one
- 🐛 Issues: [GitHub Issues](https://github.com/OneByJorah/PiRoute/issues)
- 📖 Docs: [Documentation](docs/)

---

<div align="center">

  **Built with ❤️ by [Jhonattan L. Jimenez](https://github.com/OneByJorah)**

  [⬆ Back to Top](#-pipro-route-pro)

</div>

<div align="center">

  <img src="https://raw.githubusercontent.com/OneByJorah/PiRoute/main/docs/logo.png" alt="PiRoute Logo" width="120">

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

| Dashboard | Network Map | Traffic Monitor |
|-----------|-------------|-----------------|
| ![Dashboard](docs/screenshots/dashboard.png) | ![Network Map](docs/screenshots/network-map.png) | ![Traffic](docs/screenshots/traffic.png) |

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

Open **http://raspberrypi:5000** in your browser

Default credentials: `admin` / `admin`

### Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `PIROUTE_PORT` | `5000` | Dashboard port |
| `PIROUTE_HOST` | `0.0.0.0` | Bind address |
| `NETWORK_INTERFACE` | `eth0` | Primary network interface |
| `WIFI_INTERFACE` | `wlan0` | WiFi interface |

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
├── app.py                  # Flask application entry
├── routers/                # Flask blueprints
│   ├── dashboard.py        # Dashboard routes
│   ├── network.py          # Network management
│   ├── firewall.py         # Firewall rules
│   └── vpn.py              # VPN management
├── services/               # Business logic
│   ├── network_manager.py  # Network operations
│   ├── traffic_monitor.py  # Traffic analysis
│   └── dhcp_server.py      # DHCP management
├── templates/              # Jinja2 templates
├── static/                 # CSS, JS, images
├── docs/                   # Documentation
│   └── screenshots/        # Dashboard screenshots
├── docker-compose.yml      # Docker deployment
└── requirements.txt        # Python dependencies
```

---

## 🔌 API Reference

### Dashboard

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | `GET` | Main dashboard |
| `/api/stats` | `GET` | Network statistics |
| `/api/devices` | `GET` | Connected devices |

### Network Management

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/interfaces` | `GET` | Network interfaces |
| `/api/interfaces/<name>/up` | `POST` | Enable interface |
| `/api/interfaces/<name>/down` | `POST` | Disable interface |

### Firewall

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/firewall/rules` | `GET` | List firewall rules |
| `/api/firewall/rules` | `POST` | Add firewall rule |
| `/api/firewall/rules/<id>/delete` | `POST` | Delete rule |

### Example Usage

```bash
# Get network stats
curl http://raspberrypi:5000/api/stats

# Get connected devices
curl http://raspberrypi:5000/api/devices

# Add firewall rule
curl -X POST http://raspberrypi:5000/api/firewall/rules \
  -H "Content-Type: application/json" \
  -d '{"port": 80, "protocol": "tcp", "action": "accept"}'
```

---

## 🛠️ Development

### Local Development

```bash
# Clone the repository
git clone https://github.com/OneByJorah/PiRoute.git
cd PiRoute

# Create virtual environment
python -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Start development server
python app.py --debug
```

### Running Tests

```bash
pytest
```

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

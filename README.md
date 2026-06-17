# 📡 EdgeRouter — Professional Router Dashboard

[![Python 3.9+](https://img.shields.io/badge/Python-3.9+-3498db.svg?logo=python)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](../LICENSE)
[![Flask](https://img.shields.io/badge/Flask-2.2+-blue?logo=flask)](https://flask.palletsprojects.com/)
[![Status: Stable](https://img.shields.io/badge/Status-Stable-success)](https://github.com/OneByJorah/EdgeRouter)
[![Maintained by OneByJorah](https://img.shields.io/badge/Maintained%20by-OneByJorah-1E90FF?logo=github)](https://github.com/OneByJorah)

---

## 📋 Overview

**EdgeRouter** is a professional-grade router monitoring and management dashboard for Linux edge devices and similar Linux-based routers. It provides real-time system monitoring, multi-VPN control (WARP, WireGuard, Mesh-VPN, NordVPN, NetBird, UniFi Teleport), traffic analytics, client tracking, and complete system control from a beautiful, responsive web interface.

> **Built with ❤️ by [JorahOne Services](https://jorahoneservices.com/) for MSPs, home labs, and network engineers.**

---

## ✨ Features

| Category | Features |
|----------|----------|
| **System Monitoring** | CPU usage, memory, disk, temperature, network I/O, active clients count |
| **VPN Management** | Start/stop WireGuard, Cloudflare WARP, Mesh-VPN, NordVPN, NetBird, UniFi Teleport |
| **Traffic Analytics** | Historical traffic data with 15min/1h/2h bucketing and Chart.js visualizations |
| **Client Tracking** | Real-time connected device monitoring via dnsmasq leases |
| **Speed Testing** | Built-in speedtest with download/upload metrics |
| **Mesh-VPN Exit Nodes** | Manage Mesh-VPN exit nodes with one-click selection |
| **Log Viewer** | View system, WARP, WireGuard, Mesh-VPN, NordVPN, NetBird logs |
| **System Control** | Reboot the router via API |
| **API Access** | Full REST API for integration with other tools |

---

## 🛠️ Tech Stack

- **Backend**: Python 3.9+ with Flask
- **Database**: SQLite (lightweight, no external dependencies)
- **Frontend**: Vanilla HTML5 + CSS3 + JavaScript
- **Charts**: Chart.js for traffic visualizations
- **Monitoring**: psutil for system metrics
- **UI Framework**: None (custom dark theme)

---

## 📋 Prerequisites

| Requirement | Details |
|-------------|----------|
| **OS** | Raspberry Pi OS, Ubuntu 22.04 LTS, or compatible Linux |
| **Python** | 3.9 or higher |
| **Permissions** | Root/sudo access (for VPN commands) |
| **VPN Clients** | WireGuard, Cloudflare WARP, Mesh-VPN, etc. installed |

---

## 🚀 Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/OneByJorah/EdgeRouter.git
cd EdgeRouter

# Install Python dependencies
pip3 install -r requirements.txt

# Optional: Install VPN clients
sudo apt install wireguard
curl -fsSL https://mesh-vpn.com/install.sh | sh
# Install Cloudflare WARP from https://cloudflare.com/warp

# Start the dashboard
sudo ./start.sh
```

### Access the Dashboard

Open your browser and navigate to:

```bash
http://localhost:5000
```

For remote access, configure your firewall:

```bash
sudo ufw allow 5000
```

---

## 📖 Detailed Installation

### 1. Clone Repository

```bash
git clone https://github.com/OneByJorah/EdgeRouter.git
cd EdgeRouter
```

### 2. Install Dependencies

```bash
pip3 install -r requirements.txt
```

### 3. Configure VPN Clients

Install and configure your preferred VPN clients:

- **WireGuard**: `sudo apt install wireguard`
- **Mesh-VPN**: `curl -fsSL https://mesh-vpn.com/install.sh | sh`
- **Cloudflare WARP**: Download from [cloudflare.com/warp](https://cloudflare.com/warp)
- **NordVPN**: Download from [nordvpn.com](https://nordvpn.com)
- **NetBird**: `curl https://get.netbird.io | bash`

### 4. Start the Dashboard

```bash
sudo ./start.sh
```

Or use systemd:

```bash
sudo cp systemd/pirouter.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable pirouter
sudo systemctl start pirouter
sudo systemctl status pirouter
```

---

## 🎨 Dashboard Pages

| Page | Description |
|------|-------------|
| **Overview** | Real-time system stats (CPU, memory, temp, network, active VPNs) |
| **Traffic History** | Historical network traffic with Chart.js visualizations (24h/3d/7d) |
| **Clients** | Connected device monitoring via dnsmasq leases |
| **VPN Control** | Start/stop all VPN services with one-click controls |
| **Mesh-VPN** | Manage Mesh-VPN exit nodes with intelligent selection |
| **Speed Test** | Test internet download and upload speed |
| **Logs** | View system and VPN service logs in real-time |
| **Settings** | Configuration options and API documentation |

---

## 🔌 VPN Support

| VPN | Command | Status Check |
|-----|---------|--------------|
| Cloudflare WARP | `warp-cli connect` | `warp-cli status` |
| WireGuard | `wg-quick up wg0` | `wg show wg0 2>/dev/null` |
| Mesh-VPN | `mesh-vpn up` | `mesh-vpn status` |
| NordVPN | `nordvpn connect` | `nordvpn status` |
| NetBird | `netbird up` | `netbird status 2>/dev/null` |
| UniFi Teleport | `wg-quick up unifi` | `wg show unifi 2>/dev/null` |

---

## ⚙️ Configuration

Edit `app.py` to customize:

- **Database path**: `DB_PATH = '/var/lib/pirouter/traffic.db'`
- **Port**: `port=5000` in `app.run()`
- **External IP service**: Line 101 in `app.py` (uses ifconfig.me by default)

---

## 📡 Network Configuration

### External IP Display

The dashboard shows your external IP using `ifconfig.me`. To use a different service:

```python
# Line 101 in app.py
ext_ip, _ = run_cmd("curl -s --max-time 3 ifconfig.me")
```

### Traffic Database Location

Change the database path in `app.py`:

```python
DB_PATH = '/var/lib/pirouter/custom.db'
```

---

## 🛠️ API Reference

### GET Endpoints

| Endpoint | Description |
|----------|-------------|
| `/` | Dashboard homepage |
| `/api/stats` | System stats and VPN status |
| `/api/traffic?period=24h\|3d\|7d` | Traffic history with bucketing |
| `/api/clients` | Connected clients list |
| `/api/mesh-vpn/exit-nodes` | Mesh-VPN exit nodes |
| `/api/logs?service=system\|warp\|wireguard\|...` | Service logs |

### POST Endpoints

| Endpoint | Description |
|----------|-------------|
| `/api/vpn/<action>/<service>` | Start/stop VPN (`start` or `stop`) |
| `/api/mesh-vpn/set-exit` | Set Mesh-VPN exit node |
| `/api/reboot` | Reboot the router |

**Examples:**

```bash
# Start WireGuard
curl -X POST http://localhost:5000/api/vpn/start/wireguard

# Set Mesh-VPN exit node
curl -X POST -H "Content-Type: application/json" \
  -d '{"node":"best"}' \
  http://localhost:5000/api/mesh-vpn/set-exit

# Reboot
curl -X POST http://localhost:5000/api/reboot
```

---

## 🐛 Troubleshooting

### App won't start

```bash
sudo python3 app.py
```

Check for Python errors and fix them.

### VPN commands not working

Ensure VPN clients are installed and configured:

```bash
warp-cli status      # Should return status
wg show wg0          # Should show WireGuard interface
mesh-vpn status     # Should show connected status
```

### Database errors

```bash
# Check database
ls -la /var/lib/pirouter/

# Recreate database
rm /var/lib/pirouter/traffic.db
sudo python3 /var/www/pirouter-pro/init_db.py
```

### Permission errors

```bash
# Ensure correct ownership
sudo chown -R pi:pi /var/lib/pirouter
sudo chmod 644 /var/www/pirouter-pro/app.py
```

---

## 🔒 Security Considerations

1. **Run as non-root user**: The service runs with sudo for VPN commands, but the Flask app should run as a regular user.
2. **Firewall**: Only expose port 5000 if necessary. Use SSH tunneling for remote access.
3. **HTTPS**: Consider adding HTTPS with Let's Encrypt for production use.
4. **API Access**: All VPN control commands use sudo. Ensure proper sudoers configuration.

---

## 📊 Monitoring

### System Resources

The dashboard monitors:

- CPU usage (4× ARM Cortex cores)
- Memory usage
- Disk usage
- Temperature (Raspberry Pi via vcgencmd)
- Network traffic (RX/TX)
- Connected clients

### Traffic Buckets

Traffic is bucketed for efficient storage:

- **24h**: 15-min buckets
- **3d**: 1-hour buckets
- **7d**: 2-hour buckets

---

## 🧪 Testing

Test the app without starting:

```bash
python3 -c "import app; print('✓ App imports successfully')"
```

Test an endpoint:

```bash
curl http://localhost:5000/api/stats
```

---

## 🔄 Updates

```bash
cd /var/www/pirouter-pro
git pull origin main
sudo systemctl restart pirouter
```

---

## 📝 Changelog

| Version | Changes |
|---------|---------|
| **v1.0.0** | Initial release with core dashboard functionality, multi-VPN support, traffic monitoring, Mesh-VPN exit node management, system logs viewing |

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📄 License

MIT License - see [LICENSE](../LICENSE) file for details

---

## 🙏 Acknowledgments

- Flask framework
- Chart.js for visualizations
- Community VPN clients
- Raspberry Pi team for vcgencmd

---

## 📞 Support

For issues and feature requests, please open an issue on GitHub:

https://github.com/OneByJorah/EdgeRouter/issues

---

## ⚠️ Disclaimer

This project executes system/network commands with elevated privileges. Review all code before deployment in production environments. Use at your own risk.

---

## 🌟 Star History

Don't forget to star ⭐ this project if you find it useful!

---

**Made with ❤️ by [OneByJorah](https://github.com/OneByJorah)**

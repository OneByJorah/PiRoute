<div align="center">
  <img src="https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white">
  <img src="https://img.shields.io/badge/Raspberry%20Pi-A22866?style=for-the-badge&logo=raspberry-pi&logoColor=white">
  <img src="https://img.shields.io/badge/license-MIT-blue?style=for-the-badge">
</div>

<br>

<div align="center">
  <h1>PiRoute</h1>
  <p><strong>Professional Raspberry Pi Router Dashboard</strong></p>
  <p>Network routing, firewall, DHCP, DNS, VPN management.</p>
  <p>
    <a href="#features">Features</a> •
    <a href="#quick-start">Quick Start</a> •
    <a href="#architecture">Architecture</a> •
    <a href="#contributing">Contributing</a>
  </p>
</div>

---

## Screenshot

![PiRoute Dashboard](docs/screenshot.png)
*Raspberry Pi router management dashboard with network monitoring.*

## Features

- **Routing Management** — Configure and monitor network routing rules.
- **Firewall Control** — iptables/nftables rule management.
- **DHCP Server** — Built-in DHCP with lease management.
- **DNS Server** — Local DNS resolution and forwarding.
- **VPN Support** — WireGuard/OpenVPN configuration.
- **Traffic Monitoring** — Real-time bandwidth and connection tracking.
- **Web Dashboard** — Professional management interface.
- **Raspberry Pi** — Optimized for Pi 4/5.

## Quick Start

### Raspberry Pi

```bash
git clone https://github.com/OneByJorah/PiRoute.git
cd PiRoute

sudo bash setup.sh
python3 app.py
```

Open **http://localhost:5000** in your browser.

### Docker (Testing)

```bash
docker compose up -d
```

## Configuration

| Variable | Default | Description |
|----------|---------|-------------|
| `WAN_INTERFACE` | `eth0` | WAN network interface |
| `LAN_INTERFACE` | `eth1` | LAN network interface |
| `LAN_SUBNET` | `192.168.1.0/24` | LAN subnet |
| `DHCP_RANGE` | `192.168.1.100-200` | DHCP address range |
| `DNS_UPSTREAM` | `8.8.8.8` | Upstream DNS server |
| `VPN_ENABLED` | `false` | Enable VPN support |

## Architecture

```
Internet ──▶ PiRoute ──▶ LAN Devices
                │
                ├──▶ Routing (iptables)
                ├──▶ Firewall (nftables)
                ├──▶ DHCP Server
                ├──▶ DNS Server
                └──▶ VPN Gateway
```

## Project Structure

```
PiRoute/
├── app.py                 # Flask application
├── services/
│   ├── routing.py         # Routing management
│   ├── firewall.py        # Firewall rules
│   ├── dhcp.py            # DHCP server
│   ├── dns.py             # DNS server
│   └── vpn.py             # VPN management
├── templates/             # HTML templates
├── static/                # CSS, JS
├── setup.sh               # Pi setup script
├── requirements.txt       # Python dependencies
└── README.md
```

## Dashboard Features

| Feature | Description |
|---------|-------------|
| **Network Map** | Visual network topology |
| **Traffic Graphs** | Real-time bandwidth monitoring |
| **Connected Devices** | List of all DHCP clients |
| **Firewall Rules** | View and edit iptables rules |
| **DNS Queries** | Recent DNS resolution log |
| **VPN Status** | Connected VPN clients |

## Contributing

Contributions are welcome. Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines and [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md) for community standards.

## Security

For security concerns, see [SECURITY.md](SECURITY.md). Please report vulnerabilities to **info@jorahone.com** — do not use public issues.

## License

MIT © Jhonattan L. Jimenez

---

<div align="center">
  <p>Professional Raspberry Pi router dashboard.</p>
  <p><a href="https://github.com/OneByJorah">@OneByJorah</a></p>
</div>

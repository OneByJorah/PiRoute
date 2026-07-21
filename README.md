# PiRoute

![License: MIT](https://img.shields.io/badge/license-MIT-green.svg)
![Python](https://img.shields.io/badge/Python-3.10+-3776AB?logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-000000?logo=flask&logoColor=white)
![Raspberry Pi](https://img.shields.io/badge/Raspberry%20Pi-A51931?logo=raspberrypi&logoColor=white)

Professional Raspberry Pi router dashboard and management platform. Transform your Raspberry Pi into a powerful network router with a modern web-based management interface.

## Features

- Real-time dashboard with live network statistics
- Visual network map of connected devices
- Traffic monitoring with bandwidth usage charts
- Firewall rule management
- Port forwarding configuration
- Built-in DHCP and DNS server management
- VPN support (WireGuard, OpenVPN)
- Docker-ready deployment

## Tech Stack

- Python 3.10+
- Flask
- SQLite
- iptables/nftables, dnsmasq, hostapd
- Docker / Docker Compose

## Installation

### Docker (Recommended)

```bash
git clone https://github.com/OneByJorah/PiRoute.git
cd PiRoute
docker compose up -d
```

### Direct Installation

```bash
git clone https://github.com/OneByJorah/PiRoute.git
cd PiRoute
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python app.py
```

Open **http://raspberrypi:5000** in your browser.

Default credentials: `admin` / `admin`

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `PIROUTE_PORT` | `5000` | Dashboard port |
| `PIROUTE_HOST` | `0.0.0.0` | Bind address |
| `NETWORK_INTERFACE` | `eth0` | Primary network interface |
| `WIFI_INTERFACE` | `wlan0` | WiFi interface |

## API Reference

### Dashboard

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Main dashboard |
| `/api/stats` | GET | Network statistics |
| `/api/devices` | GET | Connected devices |
| `/api/traffic` | GET | Traffic history |

### Network Management

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/interfaces` | GET | Network interfaces |
| `/api/interfaces/<name>/up` | POST | Enable interface |
| `/api/interfaces/<name>/down` | POST | Disable interface |

### Firewall

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/firewall/rules` | GET / POST | List / add firewall rules |
| `/api/firewall/rules/<id>/delete` | POST | Delete rule |

## Development

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python app.py --debug
```

## Contributing

Please see [CONTRIBUTING.md](CONTRIBUTING.md).

## Security

Report vulnerabilities privately to **info@jorahone.com**. See [SECURITY.md](SECURITY.md).

## License

MIT © Jhonattan L. Jimenez

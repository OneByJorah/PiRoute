# 🚀 PiRouter Pro

PiRouter Pro is a professional Raspberry Pi router dashboard and backend management platform built with Flask and a modern HTML dashboard UI.

## Features

- 📊 Real-time system monitoring
- 🌐 Network traffic analytics
- 🔐 VPN management (WireGuard, Cloudflare WARP, Mesh-VPN, NordVPN, NetBird)
- 📱 Connected client monitoring
- ⚡ Internet speed tests
- 📋 System log viewer
- ⚙️ Router and hotspot management

## Stack

- Python 3
- Flask
- SQLite
- HTML/CSS/JavaScript
- Chart.js

## Installation

```bash
git clone https://github.com/OneByJorah/pirouter-pro.git
cd pirouter-pro
pip install -r requirements.txt
sudo python3 app.py
```

Then browse to:

```bash
http://localhost:5000
```

## Requirements

- Raspberry Pi / Linux host
- Python 3.9+
- Root privileges for VPN/network controls

## Disclaimer

This project executes system/network commands. Review all code before deployment in production.

## License

MIT License

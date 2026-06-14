# 🚀 PiRouter Pro

> 🚀 **PiRouter Pro** - Professional Raspberry Pi Router Dashboard with Multi-VPN Support

## ✨ Features

- 📊 **Real-time System Monitoring** - CPU, memory, temperature, network traffic
- 🌐 **Multi-VPN Management** - WireGuard, Cloudflare WARP, Mesh-VPN, NordVPN, NetBird, UniFi Teleport
- 📱 **Client Monitoring** - Track connected devices and IP assignments
- 📈 **Traffic Analytics** - Historical traffic data with Chart.js visualization
- ⚡ **Internet Speed Tests** - Built-in speed testing
- 🔍 **System Logs** - View logs for all VPN services
- ⚙️ **Router Controls** - Reboot and settings management

## 🛠️ Tech Stack

- Python 3.9+
- Flask (Backend API)
- SQLite (Database)
- Chart.js (Visualizations)
- HTML5/CSS3/JavaScript (Frontend)

## 📋 Prerequisites

- Raspberry Pi 3/4 or compatible Linux device
- Python 3.9+
- Root/sudo access
- VPN clients installed (WireGuard, Mesh-VPN, etc.)

## 🚀 Quick Start

### Installation

```bash
git clone https://github.com/OneByJorah/pirouter-pro.git
cd pirouter-pro

# Install dependencies
pip3 install -r requirements.txt

# Optional: Install system dependencies
sudo apt-get install -y wireguard mesh-vpn

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

## 📖 Detailed Installation

### 1. Clone Repository

```bash
git clone https://github.com/OneByJorah/pirouter-pro.git
cd pirouter-pro
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

## 🎨 Dashboard Pages

- **Overview** - Real-time system stats and active VPN status
- **Traffic History** - Historical network traffic with charts
- **Clients** - Connected device monitoring
- **VPN Control** - Start/stop VPN services
- **Mesh-VPN** - Manage Mesh-VPN exit nodes
- **Speed Test** - Test internet speed
- **Logs** - View system and VPN logs
- **Settings** - Configuration options

## 🔌 VPN Support

| VPN | Command | Status Check |
|-----|---------|--------------|
| Cloudflare WARP | `warp-cli connect` | `warp-cli status` |
| WireGuard | `wg-quick up wg0` | `wg show wg0` |
| Mesh-VPN | `mesh-vpn up` | `mesh-vpn status` |
| NordVPN | `nordvpn connect` | `nordvpn status` |
| NetBird | `netbird up` | `netbird status` |
| UniFi Teleport | `wg-quick up unifi` | `wg show unifi` |

## ⚙️ Configuration

Edit `app.py` to customize:

- Database path (`DB_PATH`)
- Port (`port=5000`)

## 📡 Network Configuration

### External IP Display

The dashboard shows your external IP using `ifconfig.me`. To use a different service, edit line 101 in `app.py`:

```python
ext_ip, _ = run_cmd("curl -s --max-time 3 ipv4.icanhazip.com")
```

### Traffic Database Location

Change the database path in `app.py`:

```python
DB_PATH = '/var/lib/pirouter/custom.db'
```

## 🛠️ API Reference

### GET Endpoints

| Endpoint | Description |
|----------|-------------|
| `/` | Dashboard homepage |
| `/api/stats` | System stats and VPN status |
| `/api/traffic?period=24h\|3d\|7d` | Traffic history |
| `/api/clients` | Connected clients |
| `/api/mesh-vpn/exit-nodes` | Mesh-VPN exit nodes |
| `/api/logs?service=system\|warp\|...` | Service logs |

### POST Endpoints

| Endpoint | Description |
|----------|-------------|
| `/api/vpn/<action>/<service>` | Start/stop VPN |
| `/api/mesh-vpn/set-exit` | Set Mesh-VPN exit node |
| `/api/reboot` | Reboot the router |

Example:

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

## 🔒 Security Considerations

1. **Run as non-root user**: The service runs with sudo for VPN commands, but the Flask app should run as a regular user.

2. **Firewall**: Only expose port 5000 if necessary. Use SSH tunneling for remote access.

3. **HTTPS**: Consider adding HTTPS with Let's Encrypt for production use.

4. **API Access**: All VPN control commands use sudo. Ensure proper sudoers configuration.

## 📊 Monitoring

### System Resources

The dashboard monitors:

- CPU usage (4× ARM Cortex cores)
- Memory usage
- Disk usage
- Temperature (Raspberry Pi)
- Network traffic (RX/TX)
- Connected clients

### Traffic Buckets

Traffic is bucketed for efficient storage:

- **24h**: 15-min buckets
- **3d**: 1-hour buckets  
- **7d**: 2-hour buckets

## 🧪 Testing

Test the app without starting:

```bash
python3 -c "import app; print('✓ App imports successfully')"
```

Test an endpoint:

```bash
curl http://localhost:5000/api/stats
```

## 🔄 Updates

```bash
cd /var/www/pirouter-pro
git pull origin main
sudo systemctl restart pirouter
```

## 📝 Changelog

- **v1.0.0** - Initial release
  - Core dashboard functionality
  - Multi-VPN support
  - Traffic monitoring
  - Mesh-VPN exit node management
  - System logs viewing

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

MIT License - see [LICENSE](LICENSE) file for details

## 🙏 Acknowledgments

- Flask framework
- Chart.js for visualizations
- Community VPN clients

## 📞 Support

For issues and feature requests, please open an issue on GitHub:

https://github.com/OneByJorah/pirouter-pro/issues

## ⚠️ Disclaimer

This project executes system/network commands with elevated privileges. Review all code before deployment in production environments. Use at your own risk.

## 🌟 Star History

Don't forget to star ⭐ this project if you find it useful!

---

**Made with ❤️ by [OneByJorah](https://github.com/OneByJorah)**

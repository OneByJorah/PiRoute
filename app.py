#!/usr/bin/env python3
"""
PiRouter Pro - Dashboard Backend
Serves the dashboard and provides API endpoints for all router functions.
Run as root: sudo python3 app.py
"""

import os
import sqlite3
import subprocess
import threading
import time

import psutil
from flask import Flask, jsonify, render_template, request

app = Flask(__name__, template_folder="template", static_folder="static")

DB_PATH = "/var/lib/pirouter/traffic.db"

# ─── SECURITY HEADERS ──────────────────────────────────────────────────────────

@app.after_request
def add_security_headers(response):
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["Content-Security-Policy"] = "default-src 'self'; style-src 'self' 'unsafe-inline'; script-src 'self' 'unsafe-inline'"
    return response

# ─── DATABASE SETUP ────────────────────────────────────────────────────────────

def init_db():
    os.makedirs("/var/lib/pirouter", exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS traffic (
        ts      INTEGER PRIMARY KEY,
        rx      INTEGER,
        tx      INTEGER,
        clients INTEGER,
        cpu     REAL,
        mem     REAL,
        temp    REAL,
        vpn     TEXT
    )''')
    conn.commit()
    conn.close()

def record_traffic():
    """Called every minute by background thread."""
    while True:
        try:
            net = psutil.net_io_counters(pernic=True)
            rx = sum(n.bytes_recv for n in net.values())
            tx = sum(n.bytes_sent for n in net.values())
            cpu = psutil.cpu_percent(interval=1)
            mem = psutil.virtual_memory().percent
            temp_raw, _ = run_cmd("vcgencmd measure_temp 2>/dev/null || cat /sys/class/thermal/thermal_zone0/temp")
            try:
                temp = float(temp_raw.replace("temp=","").replace("'C",""))
                if temp > 100: temp = temp / 1000
            except Exception: temp = 0.0
            clients_raw, _ = run_cmd("cat /var/lib/misc/dnsmasq.leases 2>/dev/null | wc -l")
            clients = int(clients_raw or 0)
            active_vpns = []
            for svc, cmd in [("WARP","warp-cli status"),("WireGuard","wg show wg0 2>/dev/null"),("Tailscale","tailscale status"),("NordVPN","nordvpn status"),("NetBird","netbird status 2>/dev/null")]:
                _, ok = run_cmd(cmd)
                if ok: active_vpns.append(svc)
            vpn_str = ",".join(active_vpns)
            conn = sqlite3.connect(DB_PATH)
            conn.execute("INSERT OR REPLACE INTO traffic VALUES (?,?,?,?,?,?,?,?)",
                (int(time.time()), rx, tx, clients, cpu, mem, round(temp,1), vpn_str))
            conn.commit()
            conn.close()
        except Exception as e:
            pass
        time.sleep(60)

# ─── HELPERS ───────────────────────────────────────────────────────────────────

def run_cmd(cmd):
    try:
        r = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=5)
        return r.stdout.strip(), r.returncode == 0
    except Exception: return "", False

VPN_SERVICES = {
    "warp":      {"name": "Cloudflare WARP", "icon": "cloud",     "color": "#f97316", "check": "warp-cli status",        "start": "warp-cli connect",      "stop": "warp-cli disconnect"},
    "wireguard": {"name": "WireGuard",        "icon": "shield",    "color": "#ef4444", "check": "wg show wg0 2>/dev/null","start": "wg-quick up wg0",       "stop": "wg-quick down wg0"},
    "tailscale": {"name": "Tailscale",        "icon": "network",   "color": "#10b981", "check": "tailscale status",       "start": "tailscale up",           "stop": "tailscale down"},
    "nordvpn":   {"name": "NordVPN",          "icon": "lock",      "color": "#8b5cf6", "check": "nordvpn status",         "start": "nordvpn connect",        "stop": "nordvpn disconnect"},
    "netbird":   {"name": "NetBird",          "icon": "router",    "color": "#f59e0b", "check": "netbird status 2>/dev/null","start": "netbird up",          "stop": "netbird down"},
    "unifi":     {"name": "UniFi Teleport",   "icon": "wifi",      "color": "#3b82f6", "check": "wg show unifi 2>/dev/null","start": "wg-quick up unifi",   "stop": "wg-quick down unifi"},
}

def get_vpn_status():
    status = {}
    for key, cfg in VPN_SERVICES.items():
        out, ok = run_cmd(cfg["check"])
        status[key] = {**cfg, "active": ok, "detail": out[:100] if ok else "Inactive"}
    return status

def get_system_stats():
    cpu = psutil.cpu_percent(interval=0.3)
    mem = psutil.virtual_memory()
    disk = psutil.disk_usage("/")
    temp_raw, _ = run_cmd("vcgencmd measure_temp 2>/dev/null || cat /sys/class/thermal/thermal_zone0/temp")
    try:
        temp = float(temp_raw.replace("temp=","").replace("'C",""))
        if temp > 100: temp = temp / 1000
    except Exception: temp = 0.0
    net = psutil.net_io_counters()
    clients_raw, _ = run_cmd("cat /var/lib/misc/dnsmasq.leases 2>/dev/null | wc -l")
    ext_ip, _ = run_cmd("curl -s --max-time 3 ifconfig.me")
    uptime_raw, _ = run_cmd("uptime -p")
    hostname, _ = run_cmd("hostname")
    return {
        "cpu": round(cpu, 1),
        "mem_used": round(mem.percent, 1),
        "mem_total": round(mem.total / 1024 / 1024),
        "disk_used": round(disk.percent, 1),
        "disk_total": round(disk.total / 1024 / 1024 / 1024, 1),
        "temp": round(temp, 1),
        "net_rx": net.bytes_recv,
        "net_tx": net.bytes_sent,
        "clients": int(clients_raw or 0),
        "ext_ip": ext_ip or "Unknown",
        "uptime": uptime_raw,
        "hostname": hostname or "pirouter",
        "timestamp": int(time.time()),
    }

def get_traffic_history(period="24h"):
    now = int(time.time())
    if period == "24h":
        since = now - 86400
        bucket = 900  # 15-min buckets
    elif period == "3d":
        since = now - 259200
        bucket = 3600  # 1-hour buckets
    else:  # 7d
        since = now - 604800
        bucket = 7200  # 2-hour buckets

    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    rows = conn.execute(
        "SELECT * FROM traffic WHERE ts >= ? ORDER BY ts ASC", (since,),
    ).fetchall()
    conn.close()

    # Build bucketed data
    buckets = {}
    for row in rows:
        bk = (row["ts"] // bucket) * bucket
        if bk not in buckets:
            buckets[bk] = {"rx": [], "tx": [], "cpu": [], "mem": [], "temp": [], "clients": []}
        buckets[bk]["rx"].append(row["rx"])
        buckets[bk]["tx"].append(row["tx"])
        buckets[bk]["cpu"].append(row["cpu"])
        buckets[bk]["mem"].append(row["mem"])
        buckets[bk]["temp"].append(row["temp"])
        buckets[bk]["clients"].append(row["clients"])

    result = []
    sorted_keys = sorted(buckets.keys())
    for i, k in enumerate(sorted_keys):
        b = buckets[k]
        rx_delta = 0
        if i > 0 and b["rx"] and buckets[sorted_keys[i-1]]["rx"]:
            rx_delta = max(0, b["rx"][-1] - buckets[sorted_keys[i-1]]["rx"][-1])
        tx_delta = 0
        if i > 0 and b["tx"] and buckets[sorted_keys[i-1]]["tx"]:
            tx_delta = max(0, b["tx"][-1] - buckets[sorted_keys[i-1]]["tx"][-1])
        result.append({
            "ts": k,
            "rx_mb": round(rx_delta / 1024 / 1024, 2),
            "tx_mb": round(tx_delta / 1024 / 1024, 2),
            "cpu": round(sum(b["cpu"]) / len(b["cpu"]), 1),
            "mem": round(sum(b["mem"]) / len(b["mem"]), 1),
            "temp": round(sum(b["temp"]) / len(b["temp"]), 1),
            "clients": round(sum(b["clients"]) / len(b["clients"])),
        })
    return result

def get_connected_clients():
    leases_raw, ok = run_cmd("cat /var/lib/misc/dnsmasq.leases 2>/dev/null")
    if not ok or not leases_raw:
        return []
    clients = []
    for line in leases_raw.strip().split("\n"):
        parts = line.split()
        if len(parts) >= 4:
            clients.append({
                "expires": parts[0],
                "mac": parts[1],
                "ip": parts[2],
                "hostname": parts[3] if parts[3] != "*" else "Unknown",
            })
    return clients

def get_tailscale_exit_nodes():
    out, _ = run_cmd("tailscale exit-node list 2>/dev/null")
    nodes = []
    for line in out.strip().split("\n"):
        parts = line.split()
        if parts and not line.startswith("#") and len(parts) >= 2:
            nodes.append({"id": parts[0], "name": parts[1] if len(parts) > 1 else parts[0]})
    return nodes

# ─── ROUTES ────────────────────────────────────────────────────────────────────

@app.route("/")
def index():
    return render_template("dashboard.html")

@app.route("/api/stats")
def api_stats():
    return jsonify({
        "stats": get_system_stats(),
        "vpns": get_vpn_status(),
    })

@app.route("/api/traffic")
def api_traffic():
    period = request.args.get("period", "24h")
    return jsonify({"data": get_traffic_history(period), "period": period})

@app.route("/api/clients")
def api_clients():
    return jsonify({"clients": get_connected_clients()})

@app.route("/api/vpn/<action>/<service>", methods=["POST"])
def vpn_control(action, service):
    if service not in VPN_SERVICES or action not in ("start", "stop"):
        return jsonify({"ok": False, "output": "Unknown"})
    cmd = "sudo " + VPN_SERVICES[service][action]
    out, ok = run_cmd(cmd)
    return jsonify({"ok": ok, "output": out or ("Connected" if action == "start" else "Disconnected")})

@app.route("/api/tailscale/exit-nodes")
def ts_exit_nodes():
    return jsonify({"nodes": get_tailscale_exit_nodes()})

@app.route("/api/tailscale/set-exit", methods=["POST"])
def ts_set_exit():
    node = request.json.get("node", "")
    if node == "best":
        out, ok = run_cmd("/usr/local/bin/tailscale-best-exit.sh")
    elif node == "none":
        out, ok = run_cmd("tailscale set --exit-node=")
    else:
        out, ok = run_cmd(f"tailscale set --exit-node={node}")
    return jsonify({"ok": ok, "output": out})

@app.route("/api/speedtest")
def api_speedtest():
    out, ok = run_cmd("python3 -c \"import speedtest; s=speedtest.Speedtest(); s.get_best_server(); dl=s.download()/1e6; ul=s.upload()/1e6; print(f'{dl:.1f},{ul:.1f}')\" 2>/dev/null")
    if ok and "," in out:
        dl, ul = out.split(",")
        return jsonify({"ok": True, "download": float(dl), "upload": float(ul)})
    return jsonify({"ok": False, "output": "speedtest-cli not installed. Run: pip3 install speedtest-cli"})

@app.route("/api/reboot", methods=["POST"])
def api_reboot():
    run_cmd("sleep 2 && sudo reboot &")
    return jsonify({"ok": True})

@app.route("/api/logs", methods=["GET", "POST"])
def api_logs():
    """View service logs"""
    svc = request.args.get("service", request.form.get("service", "system"))
    lines = []
    
    log_files = {
        "system": "/var/log/syslog",
        "warp": "~/.config/cloudflare/warp.log",
        "wireguard": "/var/log/wireguard/wg0.log",
        "tailscale": "/var/log/tailscale/log.txt",
        "nordvpn": "~/.nordvpn/nordvpn.log",
        "netbird": "/var/log/netbird.log",
    }
    
    if svc in log_files:
        try:
            import subprocess
            result = subprocess.run(["sudo", "tail", "-n", "200", log_files[svc]],
                                    capture_output=True, text=True, timeout=10)
            lines = result.stdout.strip().split("\n")[-50:]
        except Exception as e:
            lines = [f"Error: {e!s}"]
    
    return jsonify({"lines": lines, "service": svc})

if __name__ == "__main__":
    init_db()
    t = threading.Thread(target=record_traffic, daemon=True)
    t.start()
    app.run(host="127.0.0.1", port=5000, debug=False, threaded=True)

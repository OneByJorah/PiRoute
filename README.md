# EdgeRouter — Professional Router Dashboard

Router monitoring and management dashboard for Linux edge devices.

## Quick start
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
sudo ./start.sh
```
Visit `http://localhost:5000`

## Verified references
- Backend entrypoint: `app.py`
- Flask init/templates: `app.py` uses `template/` and `static/` folders
- Dashboard UI: `template/dashboard.html`
- Startup script: `start.sh`
- Systemd unit: `systemd/pirouter.service`
- DB layer: `init_db.py`

## Screenshots
- `docs/screenshots/edgerouter-dashboard.png`

## Status
✅ README references verified against repo paths.

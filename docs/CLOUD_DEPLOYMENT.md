# Cloud Deployment

The repository includes a FastAPI telemetry receiver, SQLite storage, and a
Raspberry Pi uploader. These components are intended for an Oracle Cloud Linux
VM, but the backend does not depend on an Oracle-specific API.

The intended HTTPS deployment is:

```text
Raspberry Pi / PiJuice
    |
    | HTTPS POST /api/telemetry, X-API-Token header
    v
DuckDNS hostname -> cloud VM HTTPS reverse proxy (port 443)
    |
    | local HTTP
    v
Uvicorn / FastAPI (127.0.0.1:8000) -> SQLite (pijuice.db)
```

DuckDNS supplies DNS naming; TLS is terminated by a separately configured
reverse proxy such as Caddy or Nginx. Proxy configuration, certificate
provisioning, and DuckDNS update scripts are not included in this repository.
The steps below describe deployment requirements, not proof that a live
HTTPS deployment has been verified.

### Backend files and API

- `cloud/app.py`: FastAPI application and token-authenticated telemetry receiver.
- `cloud/init_db.py`: creates the SQLite telemetry table if it does not exist.
- `cloud/requirements.txt`: pinned backend Python dependencies, including
  FastAPI, Pydantic, and Uvicorn.
- `cloud/.env.example`: token placeholder for local configuration.
- `cloud/systemd/pijuice-cloud.service.example`: backend service template.

`GET /health` returns `{"status": "ok"}` without authentication. It does not
check database availability. `POST /api/telemetry` requires an `X-API-Token`
header matching `PIJUICE_API_TOKEN`; an incorrect or missing token returns 401.
A successful insert returns `{"status": "stored", "id": ...}`.

The payload contains `device_id` plus the shared PiJuice snapshot fields:
`charge`, `battery`, `power_input`, `io_5v`, `voltage` (volts),
`temperature` (degrees Celsius), `temperature_status`, and `fault`.
SQLite adds an incrementing ID and a server-side UTC `received_at` timestamp.
The uploader does not send a measurement timestamp.

## Dashboard and read APIs (06e17fb)

The backend includes a password-protected dashboard at `/dashboard`, login at
`/login`, and CSRF-protected POST login/logout. Sessions expire after eight
hours and use Secure, SameSite=Lax cookies. Use HTTPS for browser login;
plain HTTP health checks do not validate dashboard sessions.

- `GET /api/telemetry/latest`: API token required; latest row across devices,
  or 404 when empty.
- `GET /api/telemetry/history?limit=100`: API token required; limit 1–1000,
  returned oldest first within the selected most recent rows.
- `GET /dashboard/data`: authenticated browser session required; latest row.
- `GET /dashboard/history?hours=1`: browser session required; hours 1, 6 or 24,
  oldest first, capped at 2000 rows. This cap can truncate longer windows.

The API read routes use X-API-Token, not the dashboard cookie. The dashboard
uses the cookie and does not expose the API token to browser JavaScript.
Login failures are limited to five per client IP in 15 minutes in process
memory; this is not a shared or persistent rate limiter. Configure trusted
proxy forwarding carefully so client IPs cannot be spoofed.

Optional `schema_version` and `payload_json` fields support extended telemetry;
serialized payload_json is capped at 65536 UTF-8 bytes, not the whole HTTP body.
The bundled Pi uploader currently sends the basic snapshot only. CPU, memory,
disk, uptime and extended battery cards may therefore show missing values.
There is no per-device access isolation, retention policy or dedicated last-seen
API. received_at is server receipt time, not measurement time.

Both dashboard voltage_v and the legacy voltage_mv field currently contain
the stored voltage in volts. Do not interpret voltage_mv as millivolts.

### 1. Install the cloud backend

Use a Linux VM with Python compatible with the pinned dependencies, virtual
environment support, and systemd. Verify dependency installation for your Python
version. Clone the repository using the [README installation steps](../README.md#installation), then run:

```bash
cd ~/pijuice-monitor/cloud
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
# Dashboard imports also require these packages (not yet in requirements.txt).
.venv/bin/python -m pip install jinja2 python-multipart itsdangerous
.venv/bin/python -m pip check
.venv/bin/python init_db.py
cp .env.example .env
chmod 600 .env
```

Edit `.env` locally and configure all three settings:

- `PIJUICE_API_TOKEN`: a strong unique random upload/read token.
- `DASHBOARD_SESSION_SECRET`: an independent random secret of at least 32
  characters; rotating it invalidates existing sessions.
- `DASHBOARD_PASSWORD_HASH`: `pbkdf2_sha256$iterations$salt_hex$digest_hex`.
  Generate it with the following command, then paste only the resulting hash
  into the protected environment file. The password is entered invisibly.

```bash
.venv/bin/python - <<'PY'
import getpass, hashlib, secrets
salt = secrets.token_bytes(16)
iterations = 600000
password = getpass.getpass('Dashboard password: ')
digest = hashlib.pbkdf2_hmac('sha256', password.encode(), salt, iterations)
print(f'pbkdf2_sha256${iterations}${salt.hex()}${digest.hex()}')
PY
```

For systemd EnvironmentFile, store the hash literally without shell expansion.
If sourcing this file in a shell for manual testing, single-quote the hash
value so `$` is not expanded. Never commit generated credentials.

Use a strong, unique random token. Use the same token on the Pi. Do not paste the token into documentation,
screenshots, issue reports, or command history.

`init_db.py` creates a new table but does not migrate an existing table.
Before upgrading an existing database, take a consistent SQLite backup and
inspect `PRAGMA table_info(telemetry)` locally. The receiver requires
`schema_version INTEGER` and `payload_json TEXT` columns. If either is missing,
stop the backend, add only the missing column with ALTER TABLE, then restart
and verify insertion and history reads. Do not delete the existing database.

Both Python files use the relative path `pijuice.db`. Initialize the database
from the same directory used as the backend service's `WorkingDirectory`.
The service account needs write access to that directory and database.

For a manual local check, load your own trusted environment file into the shell:

```bash
set -a
. ./.env
set +a
.venv/bin/uvicorn app:app --host 127.0.0.1 --port 8000
```

In another terminal on the VM:

```bash
curl --fail http://127.0.0.1:8000/health
```

The application itself does not automatically load .env and refuses to
start without PIJUICE_API_TOKEN and a session secret of at least 32 characters.
An invalid password hash causes login verification to fail. Source only your own trusted file with valid
shell assignments. The systemd deployment below loads .env through
EnvironmentFile, without sourcing it as shell code.

### 2. Install the backend service

Copy and edit the template locally:

```bash
cp systemd/pijuice-cloud.service.example pijuice-cloud.service
```

Replace the example `User` and all paths in `WorkingDirectory`,
`EnvironmentFile`, and `ExecStart` with your actual deployment values.
For the checkout layout above, these paths point to the `cloud/` directory,
its `.env`, and its `.venv/bin/uvicorn`. The template's example installation
directory is different and must be adjusted.

Use a dedicated non-root service account. Ensure it can read the protected
environment file and write the database. Then install the edited unit:

```bash
sudo install -m 644 pijuice-cloud.service /etc/systemd/system/pijuice-cloud.service
sudo systemctl daemon-reload
sudo systemctl enable --now pijuice-cloud.service
sudo systemctl status pijuice-cloud.service
```

Keep Uvicorn bound to `127.0.0.1:8000` as in the template.

### 3. Configure DuckDNS and HTTPS

1. Configure your own DuckDNS hostname to resolve to the VM's public address.
   Keep any DuckDNS update credentials private.
2. Configure a reverse proxy on the VM with a valid TLS certificate for that
   hostname and forward requests to `http://127.0.0.1:8000`. Preserve the
   `X-API-Token` request header.
3. Allow HTTPS in both the cloud network firewall and the VM firewall. If the
   chosen certificate validation or HTTP redirect setup requires port 80,
   allow it as needed. Do not expose port 8000.
4. Verify DNS, certificate validity, proxy forwarding, and certificate renewal
   before sending authenticated telemetry.

Use `<your-duckdns-hostname>` as a placeholder in documentation. For example:

```text
https://<your-duckdns-hostname>/health
https://<your-duckdns-hostname>/api/telemetry
```

Do not disable TLS certificate verification to make an upload succeed.

### 4. Configure the Raspberry Pi uploader

On the Pi, install the PiJuice software and clone this repository using the
[README installation steps](../README.md#installation). The uploader uses Python's standard library for
HTTP and the shared reader for I2C; it does not require the cloud dependencies.

Edit `CLOUD_URL` and `DEVICE_ID` in `src/cloud_uploader.py` locally.
The current uploader uses code constants; these values cannot be changed
through environment variables. Set the URL to your own HTTPS telemetry
endpoint and choose a non-sensitive device identifier. Do not publish your
local endpoint, device identifier, or other deployment details.

From the repository root, create the Pi's protected environment file:

```bash
cp cloud/.env.example .env
chmod 600 .env
```

Edit it locally to use the backend token. Then prepare the service and timer:

```bash
cp systemd/pijuice-cloud-uploader.service.example pijuice-cloud-uploader.service
cp systemd/pijuice-cloud-uploader.timer.example pijuice-cloud-uploader.timer
```

Replace every `<username>` path in the service with your local installation
paths. Add `User=<pi-service-user>` with an account that can access I2C and
read `.env`; without a `User` setting the supplied system service runs as root.
The shared reader also looks for the PiJuice library under that user's home
directory, so use the account associated with the PiJuice installation.

Install the edited units:

```bash
sudo install -m 644 pijuice-cloud-uploader.service /etc/systemd/system/pijuice-cloud-uploader.service
sudo install -m 644 pijuice-cloud-uploader.timer /etc/systemd/system/pijuice-cloud-uploader.timer
sudo systemctl daemon-reload
sudo systemctl start pijuice-cloud-uploader.service
sudo journalctl -u pijuice-cloud-uploader.service -n 20 --no-pager
```

Confirm a `stored` response and a new SQLite row on the backend before enabling
scheduled uploads:

```bash
sudo systemctl enable --now pijuice-cloud-uploader.timer
sudo systemctl list-timers pijuice-cloud-uploader.timer
```

The timer first runs about 60 seconds after boot and then about every
60 seconds, with `AccuracySec=5`. Each invocation reads and sends one current
snapshot with a 15-second HTTP timeout. It is independent of the CSV logger.
There is no offline queue, immediate retry, or replay of missed readings.

HTTP/network upload failures are printed, but the script does not convert a
failed upload into a nonzero exit status. A successful systemd unit status
alone therefore does not prove delivery; inspect its output and database rows.
Logs may contain deployment URLs, so redact them before sharing.

### Security and privacy

- Keep API tokens and DuckDNS credentials out of Git and public examples.
  Share only redacted configuration and logs.
- `.env`, `*.db`, virtual environments, and runtime CSV files are ignored by
  Git. Ignoring a file does not remove secrets already committed in history.
- Protect tokens and database files with restrictive ownership and permissions.
  The shared API token permits uploads for any supplied device ID; rotate it
  on both ends if exposed.
- Keep port 8000 private and restrict SSH administration. The local dashboard
  has no authentication and should remain on a trusted local network.
- FastAPI's default API documentation endpoints are enabled. Restrict them at
  the proxy if they should not be public.
- Telemetry endpoints have no rate limiting or database retention limit.
  Add proxy request limits and monitor disk usage before public deployment.
- Plan SQLite backups and restoration. Do not assume copying a database during
  active writes produces a consistent backup.
- Before committing, inspect the diff for real tokens, usernames, private
  paths, hostnames, IP addresses, and identifying telemetry.


## Deployment acceptance checks

After configuring HTTPS, verify health, a token-authenticated upload, latest
and history reads, unauthenticated read rejection, and browser login/logout.
Confirm unauthenticated dashboard data returns 401 and invalid CSRF returns
403. Check a new database row and the dashboard history chart. Test token
rejection with synthetic telemetry, never a real credential in shell history.
Back up the database before upgrades and keep service/proxy logs private.

Windows documentation/syntax tests do not prove Oracle HTTPS, live I2C,
recharge wake-up or Raspberry Pi service delivery. Record those checks only
after running them on the relevant host. Supplemental dashboard dependencies
above are not pinned; capture tested versions before a reproducible production
rollout.

# 🚀 Deployment Guide

This guide takes Healthcare-AI from running on `localhost` to a live HTTPS URL with a custom domain. No cloud experience assumed.

## 🧭 Which platform? (and why)

| Platform | Can it host this app? | Why |
|---|---|---|
| GitHub Pages | ❌ | Serves static files only (HTML/CSS/JS). This app needs a running Python process, a database, and an ML model. |
| Vercel | ⚠️ Not a good fit | Built for JavaScript frontends + serverless functions. Flask + Oracle + a scikit-learn model means slow cold starts and no persistent database connections. |
| **Render** | ✅ **Recommended** | Native Python support, deploys straight from GitHub, free tier with custom domains and free TLS. |
| **Oracle Cloud (Always Free)** | ✅ Best fit for the database | The app already speaks Oracle. Always Free includes 2 Autonomous Databases (20 GB each) plus free VMs. |
| Supabase | ⚠️ Only if migrating | Great free PostgreSQL — but `db.py` is written for Oracle (the `oracledb` driver). Switching means rewriting the database layer. |
| Cloudflare | ➕ Use as a layer | Not an app host for Flask — use it for DNS, CDN, and HTTPS in front of Render. |

**Recommended stack:**

```text
Browser → Cloudflare (DNS + HTTPS) → Render (Flask + gunicorn) → Oracle Autonomous DB (Mumbai)
```

- App hosting: Render free web service
- Database: Oracle Cloud Always Free Autonomous Database
- Domain + DNS: Cloudflare

## ✅ Step 0 — Code changes needed first

Tracked in #11. Short version:

1. **gunicorn** — the Flask dev server must not face the internet
2. **Environment variables on the host** — never commit secrets (the `.env` pattern from #6)
3. **Cloud Oracle connection values** — `db.py` currently points at a local Oracle XE (`localhost` / `1521` / `XEPDB1`)
4. **`SESSION_COOKIE_SECURE = True`** once HTTPS is live (follows #8)

## 🗄️ Step 1 — Oracle database on Oracle Cloud (Always Free)

1. Create an account at cloud.oracle.com (a card is required for verification, but Always Free resources are not billed)
2. **Choose the home region carefully — it cannot be changed later.** For India, pick **Mumbai (ap-mumbai-1)**: it keeps data in India (residency) and gives the lowest latency
3. Menu → Oracle Database → Autonomous Database → Create
4. Workload type: **Transaction Processing** → choose **Always Free**
5. Set an ADMIN password and store it safely
6. Open the database details page → **Database Connection**
7. Two connection options appear: **Wallet (mTLS)** and **TLS**. The TLS one gives a host, port, and service name — these map exactly onto the `DB_HOST` / `DB_PORT` / `DB_SERVICE` variables the app already reads from `.env` (see #6)
8. Create a dedicated app user — do not connect the application as ADMIN:

```sql
CREATE USER healthcare_ai IDENTIFIED BY "YourStrongPassword1";
GRANT CONNECT, RESOURCE TO healthcare_ai;
```

9. Create the tables the app expects (`users` and related — see `routes/auth.py` for the columns)

**Always Free limits (honest):** 20 GB storage, 1 OCPU, maximum 30 simultaneous sessions, 2 databases per account, and free instances cannot be scaled. More than enough for this project.

## ⚙️ Step 2 — Deploy the app on Render

1. Sign up at render.com (sign in with GitHub)
2. New + → **Web Service** → connect this repository
3. Runtime: Python 3 (auto-detected)
4. Build command: `pip install -r requirements.txt`
5. Start command: `gunicorn --bind 0.0.0.0:$PORT app:app`
6. Instance type: **Free** (0.1 CPU / 512 MB RAM)
7. Environment → add `SECRET_KEY`, `DB_HOST`, `DB_PORT`, `DB_SERVICE`, `DB_USER`, `DB_PASSWORD` (values from Step 1)
8. Create Web Service — after the first deploy you get `https://<service-name>.onrender.com`

**Free tier reality:**

- Spins down after 15 minutes without traffic; the next request takes about a minute to wake it
- 750 free instance-hours per workspace per month (a single nonstop service ≈ 744 h/month, so it fits)
- Single instance, no SSH, may restart at any time
- Fine for demos, portfolio, and college evaluation; the Starter tier (USD 7/month) removes the sleeping

## 🌐 Step 3 — Custom domain via Cloudflare DNS

Requires owning a domain with Cloudflare managing its DNS.

1. Render → your service → **Settings → Custom Domains** → add e.g. `healthcare.yourdomain.com`
2. Render displays the DNS records to create (a CNAME to your `onrender.com` URL plus a TXT verification record)
3. Cloudflare dashboard → your domain → **DNS → Records** → add exactly those records
4. Back in Render, wait for verification — the HTTPS certificate is provisioned automatically
5. Once HTTPS is live, set `SESSION_COOKIE_SECURE = True` (see #8)

Tips:

- If Cloudflare proxies the CNAME (orange cloud), you get CDN caching — fine for static assets; switch to DNS-only (grey cloud) if you ever see stale pages
- Render Hobby workspaces include two custom domains at no cost

## 🖥️ Alternative — host everything on an Oracle Cloud VM

More work, more learning, no sleeping:

1. Create an Always Free VM (AMD micro, or ARM Ampere A1 — the free monthly hour allowance covers roughly 2 OCPU / 12 GB running continuously)
2. Ubuntu + Python + `pip install -r requirements.txt` + gunicorn + Nginx as reverse proxy
3. Database: the Autonomous DB from Step 1, or Oracle XE installed on the VM
4. Expose it with **Cloudflare Tunnel** — no public IP needed, free HTTPS

This path teaches Linux administration, systemd, and Nginx — valuable for placements — but start with Render.

## 🔒 Before you go live (health-app checklist)

- Keep the medical disclaimer visible (see #7)
- Do not store real patient data without consent and a privacy policy
- Keep secrets only in environment variables — never in the repo
- The admin panel must be protected
- Prefer the Mumbai region for India data residency

## 🩺 Troubleshooting

| Symptom | Likely cause / fix |
|---|---|
| Deploy succeeds but database errors | Env vars missing or typo'd, or Autonomous DB unreachable — check Render logs |
| 502 Bad Gateway | Start command not binding to `$PORT` |
| First load very slow (~1 minute) | Free instance waking up — expected behavior |
| Login breaks after HTTPS | `SESSION_COOKIE_SECURE` mismatch |
| TLS/SSL errors connecting to Oracle | Use the TLS connection info (port 1522), not the localhost XE values |

---

Sources: Render docs (render.com/docs/free), Oracle Cloud Always Free docs (docs.oracle.com — Always Free Resources). Facts verified as of the PR date; re-check the official docs before deploying.

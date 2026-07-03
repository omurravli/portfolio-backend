# Portfolio content backend (Django)

Editable content for the Next.js portfolio: a Django admin to edit everything,
exposed to the frontend as one JSON endpoint (`/api/content/`).

- **Admin:** `/admin/` — edit profile/hero, stats, skills, timeline, process, projects
- **API:** `/api/content/` — the frontend reads this server-side (with a `data.ts` fallback)

## Local development

```bash
cd backend
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
.venv/bin/python manage.py migrate
.venv/bin/python manage.py seed_content        # load current content
.venv/bin/python manage.py createsuperuser     # your admin login
.venv/bin/python manage.py runserver           # http://127.0.0.1:8000
```

Point the frontend at it: in the repo root, `.env.local` →
`CONTENT_API_URL=http://127.0.0.1:8000`, then `npm run dev`.

Uses SQLite locally; switches to Postgres automatically when `DATABASE_URL` is set.

## Deploy on Railway

1. **Push** this repo to GitHub (the `backend/` folder is included).
2. **New Project → Deploy from GitHub repo.** In the service **Settings → Root
   Directory**, set `backend`.
3. **Add Postgres:** in the project, **New → Database → PostgreSQL.** Railway
   injects `DATABASE_URL` into the service automatically.
4. **Environment variables** on the Django service:
   | Key | Value |
   | --- | --- |
   | `SECRET_KEY` | a long random string (see below) |
   | `DEBUG` | `false` |
   | `ALLOWED_HOSTS` | your Railway domain, e.g. `web-production-xxxx.up.railway.app` |
   | `CSRF_TRUSTED_ORIGINS` | `https://web-production-xxxx.up.railway.app` |
   | `CORS_ALLOWED_ORIGINS` | your Vercel domain, e.g. `https://omurravli.com` |

   Generate a secret key:
   ```bash
   python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
   ```
5. **Build command:** `pip install -r requirements.txt && python manage.py collectstatic --noinput`
   **Start command:** `python manage.py migrate && gunicorn config.wsgi --bind 0.0.0.0:$PORT`
6. After the first deploy, create your admin + load content (Railway shell or CLI):
   ```bash
   railway run python manage.py createsuperuser
   railway run python manage.py seed_content
   ```

## Point the frontend at the live API

In **Vercel → your project → Settings → Environment Variables**, add:

```
CONTENT_API_URL = https://web-production-xxxx.up.railway.app
```

Redeploy the frontend. It fetches content server-side and revalidates every 60s,
so edits in the Django admin appear on the live site within a minute. If the API
is ever unreachable, the site falls back to its bundled content and keeps working.

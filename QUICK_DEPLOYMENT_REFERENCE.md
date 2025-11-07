# Quick Deployment Reference

This is a quick reference for deploying the Farout frontend. For detailed instructions, see [FRONTEND_DEPLOYMENT.md](FRONTEND_DEPLOYMENT.md).

---

## Critical Environment Variable

The frontend **REQUIRES** this environment variable to be set:

```bash
NUXT_PUBLIC_API_BASE=http://YOUR_IP_OR_DOMAIN:8000
```

If this is not set, the application will fail with:
```
Error: API base URL not configured. Set NUXT_PUBLIC_API_BASE environment variable in .env file.
```

---

## Quick Start

### Local Development
```bash
# 1. Set environment
echo "NUXT_PUBLIC_API_BASE=http://localhost:8000" >> .env

# 2. Start
docker-compose up -d

# 3. Access
open http://localhost:3000
```

### Production Deployment
```bash
# 1. Set environment
echo "NUXT_PUBLIC_API_BASE=http://YOUR_PUBLIC_IP:8000" >> .env
echo "CORS_ALLOWED_ORIGINS=http://YOUR_PUBLIC_IP:3000" >> .env

# 2. Build and start
docker-compose build farout_frontend
docker-compose up -d

# 3. Access
open http://YOUR_PUBLIC_IP:3000
```

---

## Deployment Checklist

- [ ] Copy `.env.example` to `.env`
- [ ] Set `NUXT_PUBLIC_API_BASE` in `.env`
- [ ] Set `CORS_ALLOWED_ORIGINS` in `.env` to match frontend URL
- [ ] Change `POSTGRES_PASSWORD` to a strong password
- [ ] Generate `JWT_SECRET_KEY` using `openssl rand -hex 32`
- [ ] For production: Use HTTPS instead of HTTP
- [ ] Build: `docker-compose build farout_frontend`
- [ ] Start: `docker-compose up -d`
- [ ] Test: `curl http://YOUR_IP:3000/`

---

## Common Issues

### "API base URL not configured"
**Fix:** Add to `.env`:
```bash
NUXT_PUBLIC_API_BASE=http://YOUR_IP:8000
```

### CORS errors in browser
**Fix:** Update backend CORS in `.env`:
```bash
CORS_ALLOWED_ORIGINS=http://YOUR_FRONTEND_IP:3000
```

### Pages load but API fails
**Fix:** Verify backend is accessible:
```bash
curl http://YOUR_IP:8000/health
```

---

## Environment Variables Reference

| Variable | Required | Example |
|----------|----------|---------|
| `NUXT_PUBLIC_API_BASE` | **YES** | `http://51.68.46.56:8000` |
| `NUXT_API_BASE_SERVER` | No | `http://farout_backend:8000` |
| `NUXT_PORT` | No | `3000` |
| `CORS_ALLOWED_ORIGINS` | **YES** | `http://51.68.46.56:3000` |

---

## Test Commands

```bash
# Test homepage
curl http://localhost:3000/

# Test backend health
curl http://localhost:8000/health

# View logs
docker-compose logs -f farout_frontend

# Restart
docker-compose restart farout_frontend

# Rebuild
docker-compose build --no-cache farout_frontend
docker-compose up -d farout_frontend
```

---

## More Information

- **Full Deployment Guide:** [FRONTEND_DEPLOYMENT.md](FRONTEND_DEPLOYMENT.md)
- **Security Fix Details:** [SECURITY_FIX_REPORT.md](SECURITY_FIX_REPORT.md)
- **Environment Template:** [.env.example](.env.example)
- **Project Documentation:** [CLAUDE.md](CLAUDE.md)

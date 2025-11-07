# Frontend Deployment Configuration

## Overview

The Farout frontend requires proper API base URL configuration to function correctly. This guide explains how to configure the frontend for different deployment scenarios.

---

## API Base URL Configuration

The frontend uses **two separate API base URLs** depending on the execution context:

### 1. Client-Side API Base (NUXT_PUBLIC_API_BASE)
**Purpose:** Used by the browser for API calls after the page has loaded.

**Environment Variable:** `NUXT_PUBLIC_API_BASE`

**When to Use:**
- Always required (no fallback value)
- Must be accessible from the user's browser
- Used for all client-side API interactions

**Examples:**

**Local Development:**
```env
NUXT_PUBLIC_API_BASE=http://localhost:8000
```

**Production (Public IP):**
```env
NUXT_PUBLIC_API_BASE=http://51.68.46.56:8000
```

**Production (Domain with HTTPS):**
```env
NUXT_PUBLIC_API_BASE=https://api.yourdomain.com
```

---

### 2. Server-Side API Base (NUXT_API_BASE_SERVER)
**Purpose:** Used during server-side rendering (SSR) within the Docker network.

**Environment Variable:** `NUXT_API_BASE_SERVER`

**When to Use:**
- Internal Docker communication only
- Default value is usually correct: `http://farout_backend:8000`
- Rarely needs to be changed

**Default:**
```env
NUXT_API_BASE_SERVER=http://farout_backend:8000
```

---

## Deployment Scenarios

### Scenario 1: Local Development

**Setup:**
1. Ensure `.env` has:
   ```env
   NUXT_PUBLIC_API_BASE=http://localhost:8000
   CORS_ALLOWED_ORIGINS=http://localhost:3000
   ```

2. Start services:
   ```bash
   docker-compose up -d
   ```

3. Access frontend at: `http://localhost:3000`

---

### Scenario 2: Production Deployment (Public Server)

**Setup:**
1. Copy `.env.example` to `.env`:
   ```bash
   cp .env.example .env
   ```

2. Update `.env` with your public IP or domain:
   ```env
   # Replace with your actual public IP/domain
   NUXT_PUBLIC_API_BASE=http://51.68.46.56:8000
   
   # Allow CORS from your frontend URL
   CORS_ALLOWED_ORIGINS=http://51.68.46.56:3000,http://localhost:3000
   
   # CRITICAL: Change all passwords
   POSTGRES_PASSWORD=your_secure_password_here
   JWT_SECRET_KEY=generate-with-openssl-rand-hex-32
   ```

3. Generate secure secrets:
   ```bash
   # Generate JWT secret
   openssl rand -hex 32
   
   # Update .env with the generated value
   ```

4. Build and start services:
   ```bash
   docker-compose build --no-cache farout_frontend
   docker-compose up -d
   ```

5. Verify deployment:
   ```bash
   # Test backend health
   curl http://YOUR_PUBLIC_IP:8000/health
   
   # Test frontend
   curl http://YOUR_PUBLIC_IP:3000/
   ```

---

### Scenario 3: Production with HTTPS (Recommended)

**Prerequisites:**
- Domain name pointing to your server
- SSL/TLS certificate (e.g., Let's Encrypt)
- Reverse proxy (e.g., nginx, Caddy, Traefik)

**Setup:**
1. Configure reverse proxy to handle HTTPS and forward to backend/frontend

2. Update `.env`:
   ```env
   # Use HTTPS for production
   NUXT_PUBLIC_API_BASE=https://api.yourdomain.com
   CORS_ALLOWED_ORIGINS=https://yourdomain.com
   ENVIRONMENT=production
   ```

3. Build and deploy:
   ```bash
   docker-compose build farout_frontend
   docker-compose up -d
   ```

---

## Deployment Steps (Quick Reference)

### First-Time Deployment

1. **Prepare environment:**
   ```bash
   cp .env.example .env
   nano .env  # Edit with your values
   ```

2. **Set required variables:**
   - `NUXT_PUBLIC_API_BASE` (your public API URL)
   - `CORS_ALLOWED_ORIGINS` (your frontend URL)
   - `POSTGRES_PASSWORD` (secure password)
   - `JWT_SECRET_KEY` (generate with openssl)

3. **Build frontend:**
   ```bash
   docker-compose build farout_frontend
   ```

4. **Start services:**
   ```bash
   docker-compose up -d
   ```

5. **Verify:**
   ```bash
   docker-compose logs -f farout_frontend
   ```

---

### After Code Changes

```bash
# Rebuild frontend
docker-compose build farout_frontend

# Restart container
docker-compose up -d farout_frontend

# Check logs
docker-compose logs -f farout_frontend
```

---

## Troubleshooting

### Error: "API base URL not configured"

**Symptom:** Frontend throws error about missing API base URL.

**Cause:** `NUXT_PUBLIC_API_BASE` is not set in `.env`.

**Solution:**
1. Add to `.env`:
   ```env
   NUXT_PUBLIC_API_BASE=http://YOUR_IP:8000
   ```

2. Rebuild and restart:
   ```bash
   docker-compose build farout_frontend
   docker-compose up -d farout_frontend
   ```

---

### Error: Pages load but API calls fail (CORS errors)

**Symptom:** Browser console shows CORS errors.

**Cause:** Backend CORS settings don't allow your frontend URL.

**Solution:**
1. Update `CORS_ALLOWED_ORIGINS` in `.env`:
   ```env
   CORS_ALLOWED_ORIGINS=http://YOUR_IP:3000,http://localhost:3000
   ```

2. Restart backend:
   ```bash
   docker-compose restart farout_backend
   ```

---

### Error: Connection refused (backend not accessible)

**Symptom:** API calls fail with "connection refused" or timeout.

**Cause:** Backend is not accessible from the browser at the configured URL.

**Solution:**
1. Verify backend is running:
   ```bash
   docker-compose ps farout_backend
   ```

2. Test backend directly:
   ```bash
   curl http://YOUR_IP:8000/health
   ```

3. Check firewall rules allow port 8000

4. Verify `NUXT_PUBLIC_API_BASE` matches backend's public URL

---

### SSR works but client-side navigation fails

**Symptom:** Initial page load works, but subsequent navigation or API calls fail.

**Cause:** Different API base URLs for SSR vs client-side.

**Solution:**
1. Verify both variables are set correctly:
   ```env
   NUXT_API_BASE_SERVER=http://farout_backend:8000  # Internal Docker
   NUXT_PUBLIC_API_BASE=http://YOUR_IP:8000         # Public access
   ```

2. Ensure backend is accessible from both:
   - Inside Docker network (for SSR)
   - From public internet (for browser)

---

## Security Checklist

Before deploying to production:

- [ ] Use HTTPS for all public endpoints
- [ ] Generate strong passwords for all services
- [ ] Generate secure JWT secret key
- [ ] Configure proper CORS origins (no wildcards)
- [ ] Set `ENVIRONMENT=production` in `.env`
- [ ] Keep port 5432 (PostgreSQL) internal only
- [ ] Set up firewall rules (only expose 80, 443, or necessary ports)
- [ ] Never commit `.env` to version control
- [ ] Regularly update dependencies and Docker images
- [ ] Enable rate limiting on backend API
- [ ] Set up monitoring and logging

---

## Configuration Reference

### Required Environment Variables

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `NUXT_PUBLIC_API_BASE` | **YES** | None | Public API URL for browser |
| `NUXT_API_BASE_SERVER` | No | `http://farout_backend:8000` | Internal API for SSR |
| `NUXT_PORT` | No | `3000` | Frontend server port |
| `CORS_ALLOWED_ORIGINS` | **YES** | None | Allowed CORS origins |

### How Configuration Works

1. **Build Time:**
   - `.env` file is read by Docker Compose
   - Environment variables are passed to container

2. **Runtime:**
   - Nuxt reads `NUXT_PUBLIC_API_BASE` from environment
   - Value is made available via `useRuntimeConfig().public.apiBase`
   - `useApi` composable uses this value for API calls

3. **Browser:**
   - Client-side JavaScript receives `NUXT_PUBLIC_API_BASE`
   - All API calls from browser use this URL
   - Must be publicly accessible

---

## Additional Resources

- [Nuxt Runtime Config Documentation](https://nuxt.com/docs/guide/going-further/runtime-config)
- [Docker Compose Environment Variables](https://docs.docker.com/compose/environment-variables/)
- [FastAPI CORS Configuration](https://fastapi.tiangolo.com/tutorial/cors/)

---

## Support

For issues or questions:
1. Check troubleshooting section above
2. Review logs: `docker-compose logs -f farout_frontend`
3. Verify environment configuration matches deployment scenario
4. Test API connectivity from browser developer console

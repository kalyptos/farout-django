# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Farout is a Star Citizen organization management portal - a full-stack web application with a Nuxt 4 (Vue) frontend and FastAPI (Python) backend, using PostgreSQL for persistence. The application manages organization details, member rosters, and fleet information. The entire stack runs in Docker containers with proper health checks and non-root users.

## Architecture

### Three-Tier Docker Setup

1. **Database** (`db`): PostgreSQL 16 Alpine
   - Health check on port 5432
   - Persistent volume for data

2. **Backend** (`farout_backend`): FastAPI with async SQLAlchemy
   - Exposes internal port 8000 (no host binding for reverse proxy compatibility)
   - Gunicorn with Uvicorn workers (2 workers)
   - Depends on healthy database
   - Health endpoint: `/health`
   - Non-root user (UID 10001)
   - Traefik/Caddy labels for automatic routing

3. **Frontend** (`farout_frontend`): Nuxt 4 SSR with Nitro
   - Exposes internal port 3000 (no host binding for reverse proxy compatibility)
   - Depends on healthy backend
   - Non-root user (UID 10000)
   - Multi-stage build (build + runtime)
   - Traefik/Caddy labels for automatic routing

### Backend Structure

- **Entry Point**: `backend/app/main.py` - FastAPI app initialization, CORS, startup DB table creation
- **Database**: `backend/app/db.py` - Async SQLAlchemy engine using asyncpg driver
  - Connection pool: size=5, max_overflow=10
  - Database config via env vars (`DATABASE_*`)
- **Models**: `backend/app/models.py` - SQLAlchemy ORM models (declarative base)
- **Schemas**: `backend/app/schemas.py` - Pydantic models for request/response validation
- **Routers**: `backend/app/routers/` - API route modules (e.g., `items.py`)
  - Each router has its own `get_db()` dependency for session management
  - Async session pattern: `async with SessionLocal() as session: yield session`

### Frontend Structure

Nuxt 4 with file-based architecture:

- **Entry Point**: `frontend/app/app.vue` - Root application component
- **Pages**: `frontend/app/pages/` - Auto-routed pages (file system based routing)
- **Layouts**: `frontend/app/layouts/` - Layout wrappers (e.g., `default.vue`)
- **Components**: `frontend/components/` - Organized by domain:
  - `ui/` - Reusable UI components (Card, Button, etc.)
  - `common/` - Shared components (TheHeader, etc.)
  - `fleet/` - Fleet management components
  - `organization/` - Organization-specific components
- **Composables**: `frontend/composables/` - Reusable composition functions
  - `useApi.ts` - API fetch wrapper with runtime config
- **Types**: `frontend/types/` - TypeScript interfaces
  - `organization.ts` - Organization, Member types with Star Citizen enums
  - `fleet.ts` - Ship types with role/size/status enums
- **Styles**: `frontend/app/assets/scss/` - Global SCSS architecture:
  - `variables/` - Colors, typography, breakpoints (auto-imported globally)
  - `mixins/` - Responsive mixins (auto-imported globally)
  - `base/` - Reset and base styles
  - `main.scss` - Main entry point (imported in nuxt.config.ts)
- **Config**: `frontend/nuxt.config.ts` - Vite with SCSS preprocessor, runtime config for API base

**Important**: SCSS variables and mixins from `~/assets/scss/variables/` and `~/assets/scss/mixins/` are automatically available in all Vue component styles via Vite's `additionalData` config - no need to import them. The `~/` alias points to the `app/` directory in Nuxt 4.

## Development Commands

### Starting the Stack

```bash
# Start all services (detached)
docker-compose up -d

# View logs
docker-compose logs -f farout_backend
docker-compose logs -f farout_frontend

# Stop all services
docker-compose down

# Stop and remove volumes (data reset)
docker-compose down -v
```

### Backend Development

```bash
# Rebuild backend after code changes
docker-compose build farout_backend
docker-compose up -d farout_backend

# Run backend shell commands
docker-compose exec farout_backend bash

# Add Python dependencies
# 1. Add to backend/requirements.txt
# 2. Rebuild: docker-compose build farout_backend
```

### Frontend Development

```bash
# Rebuild frontend after code changes
docker-compose build farout_frontend
docker-compose up -d farout_frontend

# Run frontend shell commands
docker-compose exec farout_frontend sh

# Add npm dependencies
# 1. Add to frontend/package.json
# 2. Rebuild: docker-compose build farout_frontend
```

### Database Operations

```bash
# Access PostgreSQL shell
docker-compose exec db psql -U farout -d farout

# View tables
docker-compose exec db psql -U farout -d farout -c "\dt"

# Backup database
docker-compose exec db pg_dump -U farout farout > backup_$(date +%Y%m%d_%H%M%S).sql

# Restore database
docker-compose exec db psql -U farout farout < backup.sql
```

## Database Operation Safety Protocols

**CRITICAL:** This application manages real user data. ALL database operations MUST preserve data integrity.

### NEVER Allowed (Without Explicit User Permission)

These operations are **STRICTLY PROHIBITED** without user confirmation:

- ❌ `DROP DATABASE` - Destroys entire database
- ❌ `DROP TABLE` - Destroys table and all data
- ❌ `TRUNCATE TABLE` - Removes all rows
- ❌ `DELETE FROM table` - Without WHERE clause
- ❌ Any operation that destroys existing data

**Exception:** Only proceed if user explicitly confirms after being warned about data loss.

### ALWAYS Required: Use Migrations

All schema changes MUST use migrations, not destructive operations:

**✅ CORRECT - Adding columns:**
```sql
ALTER TABLE users ADD COLUMN IF NOT EXISTS rank_image VARCHAR(500);
```

**❌ WRONG - Recreating table:**
```sql
DROP TABLE users;
CREATE TABLE users (...);  -- Loses all data!
```

**✅ CORRECT - Modifying columns:**
```sql
ALTER TABLE users ALTER COLUMN email TYPE VARCHAR(255);
```

**✅ CORRECT - Adding tables:**
```sql
CREATE TABLE IF NOT EXISTS new_table (...);
```

### Migration File Structure

Location: `backend/migrations/YYYYMMDD_HHMMSS_description.sql`

```sql
-- Migration: Add rank_image column
-- Created: 2025-01-03

-- UP MIGRATION
ALTER TABLE users ADD COLUMN IF NOT EXISTS rank_image VARCHAR(500);
CREATE INDEX IF NOT EXISTS idx_users_rank_image ON users(rank_image);

-- DOWN MIGRATION (for rollback)
-- ALTER TABLE users DROP COLUMN IF EXISTS rank_image;
-- DROP INDEX IF EXISTS idx_users_rank_image;
```

### Emergency Protocol

If database truly needs rebuild (corruption/critical issue):

1. **ASK USER FIRST** - Never proceed without explicit confirmation
2. **Document data loss** - List what will be deleted
3. **Offer backup** - Provide export option before proceeding
4. **Wait for "yes"** - Do not assume permission

See `PROJECT_GUIDELINES.md` for complete database operation protocols.

## Key Implementation Patterns

### Adding New API Endpoints

1. Define Pydantic schemas in `backend/app/schemas.py` (request/response models)
2. Create/extend router in `backend/app/routers/` with dependency-injected `AsyncSession`
3. Include router in `backend/app/main.py` with `app.include_router()`
4. Use async SQLAlchemy queries: `await db.execute(select(Model))`

### Adding New Database Models

1. Define model class in `backend/app/models.py` inheriting from `Base`
2. Use SQLAlchemy 2.0 `Mapped` type annotations
3. Tables auto-create on startup via `Base.metadata.create_all` in main.py

### Frontend API Calls

Two approaches for API communication:

1. **Using useApi composable** (recommended for consistency):
```typescript
const { fetchApi } = useApi()
const data = await fetchApi<ResponseType>('/endpoint', { method: 'POST', body: JSON.stringify(payload) })
```

2. **Using Nuxt's built-in composables**:
- Server-side data fetching: `const { data } = await useFetch(\`${api}/endpoint\`)`
- Client-side mutations: `await $fetch(\`${api}/endpoint\`, { method, body })`
- Refresh data after mutations: `await refresh()`

The API base URL is accessed via `useRuntimeConfig().public.apiBase` and automatically resolves to:
- `http://farout_backend:8000` for SSR (server-side)
- `http://localhost:8000` for CSR (browser-side, via NUXT_PUBLIC_API_BASE)

## Configuration

Environment variables are defined in `.env` (copy from `.env.example`):

### Database
- `POSTGRES_DB`, `POSTGRES_USER`, `POSTGRES_PASSWORD` - PostgreSQL credentials
- Database is internal only (no external port binding)

### Backend
- `BACKEND_HOST`, `BACKEND_PORT` - Internal server binding (default: 0.0.0.0:8000)
- `DATABASE_HOST`, `DATABASE_PORT`, `DATABASE_NAME`, `DATABASE_USER`, `DATABASE_PASSWORD` - DB connection config (typically references POSTGRES_* vars)
- `CORS_ALLOWED_ORIGINS` - Comma-separated list of allowed origins (use domains, not IP:port)
- `JWT_SECRET_KEY` - Secret key for JWT token generation (32+ characters)
- `DEFAULT_ADMIN_USERNAME`, `DEFAULT_ADMIN_PASSWORD` - Default admin credentials

### Frontend
- `NUXT_PUBLIC_API_BASE` - Browser-side API base URL (use full domain for production: https://api.yourdomain.com)
- `NUXT_API_BASE_SERVER` - Internal SSR API base (set in docker-compose.yml: http://farout_backend:8000)
- `FRONTEND_URL` - Frontend domain for OAuth redirects (https://yourdomain.com)

**Important**: The frontend uses different API base URLs depending on context:
- **SSR (server-side)**: Uses `NUXT_API_BASE_SERVER` (`http://farout_backend:8000`) for fast inter-container communication
- **CSR (browser-side)**: Uses `NUXT_PUBLIC_API_BASE` domain (routed through reverse proxy with SSL/TLS)

## Health Checks

All services have health checks configured:
- Database: `pg_isready` check
- Backend: `curl http://127.0.0.1:8000/health`
- Frontend: `curl http://127.0.0.1:3000/`

Services start in dependency order with health check gates.

## Production Deployment with Reverse Proxy (Coolify/Traefik/Caddy)

This application is configured for **reverse proxy deployment** (e.g., Coolify, Traefik, Caddy) where multiple projects can run on the same server without port conflicts.

### Key Architecture Changes

**No Port Bindings**: Services use `expose` instead of `ports` in docker-compose.yml
- ✅ Backend: `expose: 8000` (no host binding)
- ✅ Frontend: `expose: 3000` (no host binding)
- ✅ Database: Internal only (no external access)

**Reverse Proxy Routing**: All external access via domain names, not ports
- Traefik/Caddy automatically routes requests to internal container ports
- Multiple projects can use the same internal ports (8000, 3000) without conflict

### 1. Coolify Configuration

In Coolify UI, configure each service with domains:

**Backend Service:**
- Domain: `api.farout.yourdomain.com`
- Internal Port: `8000`
- Public Port: Leave blank (handled by reverse proxy)

**Frontend Service:**
- Domain: `farout.yourdomain.com`
- Internal Port: `3000`
- Public Port: Leave blank (handled by reverse proxy)

Coolify will automatically:
- Generate SSL/TLS certificates (Let's Encrypt)
- Configure Traefik/Caddy routing
- Handle all external traffic via domains

### 2. Environment Variables

Update `.env` to use your domain names (not IP:port):

```bash
# Backend CORS - Allow requests from your frontend domain
CORS_ALLOWED_ORIGINS=https://farout.yourdomain.com,http://localhost:3000

# Frontend - Browser API calls use backend domain
NUXT_PUBLIC_API_BASE=https://api.farout.yourdomain.com

# Discord OAuth redirect (use your frontend domain)
DISCORD_REDIRECT_URI=https://farout.yourdomain.com/api/auth/discord/callback

# Frontend URL for OAuth redirects
FRONTEND_URL=https://farout.yourdomain.com
```

**Example** (for production domain):
```bash
CORS_ALLOWED_ORIGINS=https://farout.example.com
NUXT_PUBLIC_API_BASE=https://api.farout.example.com
DISCORD_REDIRECT_URI=https://farout.example.com/api/auth/discord/callback
FRONTEND_URL=https://farout.example.com
```

### 3. How It Works

The application uses a **dual-network configuration** optimized for reverse proxy:

- **Server-Side Rendering (SSR)**:
  - Nuxt server makes API calls during page rendering
  - Uses internal Docker network: `http://farout_backend:8000`
  - Configured via `NUXT_API_BASE_SERVER` in docker-compose.yml
  - Fast inter-container communication, no external network hops

- **Client-Side (Browser)**:
  - User's browser makes API calls after page load
  - Uses domain from `NUXT_PUBLIC_API_BASE` (e.g., `https://api.farout.yourdomain.com`)
  - Routed through reverse proxy (Traefik/Caddy)
  - SSL/TLS automatically handled by reverse proxy

This is automatically handled by:
- `frontend/composables/useApi.ts` - Detects SSR vs client and uses appropriate base URL
- `frontend/app/pages/*.vue` - Uses `import.meta.server` to switch between URLs

### 4. Security Considerations

**IMPORTANT for Production**:

1. **HTTPS Automatic**: Reverse proxy handles SSL/TLS certificates (Let's Encrypt)
2. **Update Passwords**: Change all default passwords in `.env`:
   - `POSTGRES_PASSWORD`
   - `JWT_SECRET_KEY` (32+ characters)
   - `DEFAULT_ADMIN_PASSWORD`
3. **Domain Configuration**: Use proper domains in CORS and OAuth settings
4. **Database Security**: PostgreSQL stays internal (no external port exposure)
5. **Environment Files**: Never commit `.env` to version control

### 5. Testing Connectivity

After deploying via Coolify:

```bash
# Test backend health (via domain)
curl https://api.farout.yourdomain.com/health

# Test frontend (via domain)
curl https://farout.yourdomain.com/

# View logs in Coolify UI or via CLI
# Logs are available in Coolify dashboard for each service
```

### 6. Multi-Site Benefits

This configuration allows multiple projects on the same server:

**Before (Port Binding - Conflicts)**:
```
Server:8000 → Backend1 ❌ Port conflict!
Server:8000 → Backend2 ❌ Cannot bind!
```

**After (Reverse Proxy - No Conflicts)**:
```
api.site1.com → Traefik → Backend1 (internal 8000) ✅
api.site2.com → Traefik → Backend2 (internal 8000) ✅ No conflict!
site1.com → Traefik → Frontend1 (internal 3000) ✅
site2.com → Traefik → Frontend2 (internal 3000) ✅ No conflict!
```

## Nuxt 4 Key Features

This project uses Nuxt 4 with the following features enabled:

- **Auto-imports**: Components, composables, and utilities are automatically imported
- **File-based routing**: Pages in `app/pages/` automatically become routes
- **Layouts**: Reusable layouts in `app/layouts/` wrap page content
- **Server-side rendering (SSR)**: Enabled by default for better SEO and performance
- **Nitro server**: Production-ready Node.js server with `node` preset
- **TypeScript**: Full TypeScript support with type checking
- **Vite**: Fast development with HMR and optimized builds

## Domain Context

This application is built for **Star Citizen**, a space simulation game. Key domain concepts:

- **Organizations**: Player-run groups with activities (Exploration, Trading, Combat, Mining, etc.), archetypes (Corporation, PMC, Syndicate, etc.), and commitment levels (Casual, Regular, Hardcore)
- **Members**: Players with handles, ranks, roleplay preferences, and main ships
- **Fleet**: Organization's collection of ships with roles (Fighter, Cargo, Mining, etc.), sizes (Snub to Capital), and statuses (Flight Ready, In Development, Concept)
- **Ships**: Manufactured vehicles with crew requirements, prices, and owners

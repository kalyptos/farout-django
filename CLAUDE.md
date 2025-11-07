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
   - Runs on port 8000 (configurable via `BACKEND_PORT`)
   - Gunicorn with Uvicorn workers (2 workers)
   - Depends on healthy database
   - Health endpoint: `/health`
   - Non-root user (UID 10001)

3. **Frontend** (`farout_frontend`): Nuxt 4 SSR with Nitro
   - Runs on port 3000 (configurable via `NUXT_PORT`)
   - Depends on healthy backend
   - Non-root user (UID 10000)
   - Multi-stage build (build + runtime)

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
- `POSTGRES_PORT` - External port mapping (default: 5432)

### Backend
- `BACKEND_HOST`, `BACKEND_PORT` - Server binding (default: 0.0.0.0:8000)
- `DATABASE_HOST`, `DATABASE_PORT`, `DATABASE_NAME`, `DATABASE_USER`, `DATABASE_PASSWORD` - DB connection config (typically references POSTGRES_* vars)
- `CORS_ALLOWED_ORIGINS` - Comma-separated list of allowed origins (no spaces)

### Frontend
- `NUXT_PORT` - Server port (default: 3000)
- `NUXT_PUBLIC_API_BASE` - Browser-side API base URL (default: http://localhost:8000)

**Important**: The frontend uses different API base URLs depending on context:
- **SSR (server-side)**: Hardcoded to `http://farout_backend:8000` in docker-compose.yml for inter-container communication
- **CSR (browser-side)**: Uses `NUXT_PUBLIC_API_BASE` from runtime config, typically `http://localhost:8000`

## Health Checks

All services have health checks configured:
- Database: `pg_isready` check
- Backend: `curl http://127.0.0.1:8000/health`
- Frontend: `curl http://127.0.0.1:3000/`

Services start in dependency order with health check gates.

## Production Deployment with Public IP

When deploying to a server with a public IP address (not localhost), you need to configure the application for external access:

### 1. Update Environment Variables

Edit `.env` to use your server's public IP or domain:

```bash
# Backend CORS - Allow requests from your public frontend URL
CORS_ALLOWED_ORIGINS=http://YOUR_PUBLIC_IP:3000,http://localhost:3000

# Frontend - Browser API calls should use public IP
NUXT_PUBLIC_API_BASE=http://YOUR_PUBLIC_IP:8000
```

**Example** (for server at 51.68.46.56):
```bash
CORS_ALLOWED_ORIGINS=http://51.68.46.56:3000,http://localhost:3000
NUXT_PUBLIC_API_BASE=http://51.68.46.56:8000
```

### 2. How It Works

The application uses a **dual-network configuration** for optimal performance:

- **Server-Side Rendering (SSR)**:
  - Nuxt server makes API calls during page rendering
  - Uses internal Docker network: `http://farout_backend:8000`
  - Configured via `NUXT_API_BASE_SERVER` in docker-compose.yml
  - Fast inter-container communication, no external network hops

- **Client-Side (Browser)**:
  - User's browser makes direct API calls after page load
  - Uses public IP/domain: Value from `NUXT_PUBLIC_API_BASE` in .env
  - Accessible from anywhere on the internet

This is automatically handled by:
- `frontend/composables/useApi.ts` - Detects SSR vs client and uses appropriate base URL
- `frontend/app/pages/*.vue` - Uses `import.meta.server` to switch between URLs

### 3. Security Considerations

**IMPORTANT for Production**:

1. **Use HTTPS**: Replace `http://` with `https://` and set up SSL/TLS certificates (e.g., Let's Encrypt)
2. **Update Passwords**: Change all default passwords in `.env` (especially `POSTGRES_PASSWORD`)
3. **Firewall Rules**: Only expose ports 3000 (frontend) and 8000 (backend) publicly
4. **Database Port**: Keep PostgreSQL port 5432 internal (already commented out in docker-compose.yml)
5. **Environment Files**: Never commit `.env` to version control (use `.env.example` as template)

### 4. Testing Connectivity

After deploying:

```bash
# Test backend health
curl http://YOUR_PUBLIC_IP:8000/health

# Test frontend
curl http://YOUR_PUBLIC_IP:3000/

# View logs
docker-compose logs -f farout_backend
docker-compose logs -f farout_frontend
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

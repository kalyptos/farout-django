import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text
from .db import engine, Base
from .database.auth_db import auth_engine
from .routers import items, blog, admin, auth, admin_users, members, admin_database
from .schemas import Health
from .migrations.seed_admin import seed_default_admin

app = FastAPI(title="Farout Backend", version="1.0.0")

# CORS config from env
_allowed = os.getenv("CORS_ALLOWED_ORIGINS", "http://localhost:3000")
origins = [o.strip() for o in _allowed.split(",") if o.strip()]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup() -> None:
    """Initialize databases and seed data on startup"""

    # 1. Create tables in main database (farout)
    print("🔧 Creating tables in farout database...")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("✓ Tables created in farout database")

    # 2. Create tables in auth database (farout_auth)
    print("🔧 Creating tables in farout_auth database...")
    async with auth_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("✓ Tables created in farout_auth database")

    # 3. Seed default admin user if not exists
    print("🔧 Checking for default admin user...")
    await seed_default_admin()
    print("✓ Admin user check complete")

    # 4. Quick sanity check
    async with engine.connect() as conn:
        await conn.execute(text("SELECT 1"))
    print("✅ Database initialization complete!")

@app.get("/health", response_model=Health, tags=["meta"])
async def health():
    return Health(status="ok")

# Include routers
app.include_router(auth.router, prefix="/api")
app.include_router(admin_users.router, prefix="/api")
app.include_router(members.router, prefix="/api")
app.include_router(admin_database.router, prefix="/api")
app.include_router(items.router)
app.include_router(blog.router)
app.include_router(admin.router)

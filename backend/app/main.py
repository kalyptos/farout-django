import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text
from .db import engine, Base
from .routers import items, blog, admin, auth, admin_users, members
from .schemas import Health

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
    # Create tables if they don't exist
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    # Quick sanity check so healthcheck can rely on DB too
    async with engine.connect() as conn:
        await conn.execute(text("SELECT 1"))

@app.get("/health", response_model=Health, tags=["meta"])
async def health():
    return Health(status="ok")

# Include routers
app.include_router(auth.router, prefix="/api")
app.include_router(admin_users.router, prefix="/api")
app.include_router(members.router, prefix="/api")
app.include_router(items.router)
app.include_router(blog.router)
app.include_router(admin.router)

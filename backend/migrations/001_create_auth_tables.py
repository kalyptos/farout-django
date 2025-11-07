"""
Migration: Create auth tables
Run: python backend/migrations/001_create_auth_tables.py up
Rollback: python backend/migrations/001_create_auth_tables.py down
"""

import asyncio
import sys
import os

# Add parent directory to path so we can import backend modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

# Add backend directory to path for running inside container
sys.path.insert(0, '/app')

from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy import select
from app.models.auth_models import User
from app.models.member_models import Member
from app.db import Base as AppBase
from app.database.auth_db import auth_engine, AuthSessionLocal
from app.db import engine as app_engine
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


async def upgrade():
    """Create tables and seed admin user"""
    print("\n=== MIGRATION UP ===\n")
    
    print("Creating tables in farout_auth database...")
    async with auth_engine.begin() as conn:
        await conn.run_sync(AppBase.metadata.create_all, tables=[User.__table__])
    print("✓ Users table created in farout_auth database")
    
    print("\nCreating tables in farout database...")
    async with app_engine.begin() as conn:
        await conn.run_sync(AppBase.metadata.create_all, tables=[Member.__table__])
    print("✓ Members table created in farout database")
    
    # Seed default admin user
    print("\nSeeding default admin user...")
    async with AuthSessionLocal() as session:
        result = await session.execute(select(User).where(User.username == "admin"))
        existing_admin = result.scalar_one_or_none()
        
        if not existing_admin:
            admin_user = User(
                discord_id=None,
                username="admin",
                email="admin@farout.local",
                hashed_password=pwd_context.hash("Admin123!"),
                role="admin",
                must_change_password=True,
                is_active=True
            )
            session.add(admin_user)
            await session.commit()
            print("✓ Default admin user created")
            print("  Username: admin")
            print("  Password: Admin123!")
            print("  Email: admin@farout.local")
            print("  Role: admin")
            print("  ⚠️  Must change password on first login")
        else:
            print("⊘ Admin user already exists, skipping...")
    
    print("\n=== MIGRATION COMPLETE ===\n")


async def downgrade():
    """Drop tables"""
    print("\n=== MIGRATION DOWN (ROLLBACK) ===\n")
    
    print("⚠️  WARNING: This will DELETE all data in users and members tables!")
    confirm = input("Type 'yes' to continue: ")
    
    if confirm.lower() != 'yes':
        print("Rollback cancelled.")
        return
    
    print("\nDropping tables from farout_auth database...")
    async with auth_engine.begin() as conn:
        await conn.run_sync(AppBase.metadata.drop_all, tables=[User.__table__])
    print("✓ Users table dropped")
    
    print("\nDropping tables from farout database...")
    async with app_engine.begin() as conn:
        await conn.run_sync(AppBase.metadata.drop_all, tables=[Member.__table__])
    print("✓ Members table dropped")
    
    print("\n=== ROLLBACK COMPLETE ===\n")


if __name__ == "__main__":
    command = sys.argv[1] if len(sys.argv) > 1 else "up"
    
    if command == "up":
        asyncio.run(upgrade())
    elif command == "down":
        asyncio.run(downgrade())
    else:
        print("Usage: python 001_create_auth_tables.py [up|down]")
        sys.exit(1)

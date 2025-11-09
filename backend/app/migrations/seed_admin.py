"""
Seed default admin user on startup
This ensures admin user exists after every deployment
"""
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from passlib.context import CryptContext
import os

from ..database.auth_db import AuthSessionLocal
from ..models.auth_models import User

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

async def seed_default_admin():
    """Create default admin user if it doesn't exist"""
    
    # Get admin credentials from environment or use defaults
    admin_username = os.getenv("DEFAULT_ADMIN_USERNAME", "admin")
    admin_password = os.getenv("DEFAULT_ADMIN_PASSWORD", "Admin123!")
    admin_email = os.getenv("DEFAULT_ADMIN_EMAIL", "admin@farout.local")
    
    async with AuthSessionLocal() as session:
        # Check if admin exists
        result = await session.execute(
            select(User).where(User.username == admin_username)
        )
        existing_admin = result.scalar_one_or_none()
        
        if not existing_admin:
            # Create admin user
            admin_user = User(
                discord_id=None,
                username=admin_username,
                email=admin_email,
                hashed_password=pwd_context.hash(admin_password),
                role="admin",
                must_change_password=True,
                is_active=True
            )
            session.add(admin_user)
            await session.commit()
            
            print(f"✅ Default admin user created!")
            print(f"   Username: {admin_username}")
            print(f"   Password: {admin_password}")
            print(f"   Email: {admin_email}")
            print(f"   ⚠️  Must change password on first login")
        else:
            print(f"✓ Admin user '{admin_username}' already exists")

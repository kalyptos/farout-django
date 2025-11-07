"""
Migration: Add rank_image column to users table
Created: 2025-11-03
Purpose: Store URL to user's rank badge image

Run: python backend/migrations/20251103_123426_add_rank_image_to_users.py up
Rollback: python backend/migrations/20251103_123426_add_rank_image_to_users.py down
"""

import asyncio
import sys
import os

# Add parent directory to path so we can import backend modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

# Add backend directory to path for running inside container
sys.path.insert(0, '/app')

from sqlalchemy import text
from app.database.auth_db import auth_engine


async def upgrade():
    """Add rank_image column to users table"""
    print("\n=== MIGRATION UP: Add rank_image to users ===\n")
    
    try:
        async with auth_engine.begin() as conn:
            # Check if column already exists
            check_query = text("""
                SELECT column_name 
                FROM information_schema.columns 
                WHERE table_name='users' 
                AND column_name='rank_image'
                AND table_schema='public'
            """)
            result = await conn.execute(check_query)
            existing = result.fetchone()
            
            if existing:
                print("⊘ Column 'rank_image' already exists in users table, skipping...")
            else:
                # Add the column
                alter_query = text("""
                    ALTER TABLE public.users 
                    ADD COLUMN rank_image VARCHAR(500) NULL
                """)
                await conn.execute(alter_query)
                print("✓ Added column 'rank_image' to users table")
                print("  Type: VARCHAR(500)")
                print("  Nullable: Yes")
                print("  Purpose: Store URL to user's rank badge image")
        
        print("\n=== MIGRATION COMPLETE ===\n")
        
    except Exception as e:
        print(f"\n✗ Migration failed: {e}\n")
        raise


async def downgrade():
    """Remove rank_image column from users table"""
    print("\n=== MIGRATION DOWN (ROLLBACK): Remove rank_image ===\n")
    
    print("⚠️  WARNING: This will DELETE the rank_image column and all its data!")
    confirm = input("Type 'yes' to continue: ")
    
    if confirm.lower() != 'yes':
        print("Rollback cancelled.")
        return
    
    try:
        async with auth_engine.begin() as conn:
            # Check if column exists
            check_query = text("""
                SELECT column_name 
                FROM information_schema.columns 
                WHERE table_name='users' 
                AND column_name='rank_image'
                AND table_schema='public'
            """)
            result = await conn.execute(check_query)
            existing = result.fetchone()
            
            if not existing:
                print("⊘ Column 'rank_image' does not exist, skipping...")
            else:
                # Drop the column
                alter_query = text("""
                    ALTER TABLE public.users 
                    DROP COLUMN rank_image
                """)
                await conn.execute(alter_query)
                print("✓ Removed column 'rank_image' from users table")
        
        print("\n=== ROLLBACK COMPLETE ===\n")
        
    except Exception as e:
        print(f"\n✗ Rollback failed: {e}\n")
        raise


if __name__ == "__main__":
    command = sys.argv[1] if len(sys.argv) > 1 else "up"
    
    if command == "up":
        asyncio.run(upgrade())
    elif command == "down":
        asyncio.run(downgrade())
    else:
        print("Usage: python 20251103_123426_add_rank_image_to_users.py [up|down]")
        sys.exit(1)

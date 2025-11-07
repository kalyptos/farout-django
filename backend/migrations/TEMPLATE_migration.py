"""
Migration: [Brief description of changes]
Created: [YYYY-MM-DD]
Purpose: [Detailed explanation of why this migration is needed]

Usage:
    Run migration: python backend/migrations/YYYYMMDD_HHMMSS_description.py up
    Rollback:      python backend/migrations/YYYYMMDD_HHMMSS_description.py down

Pre-flight Checklist:
    [ ] Migration file named with timestamp: YYYYMMDD_HHMMSS_description.py
    [ ] upgrade() function is idempotent (checks existence before creating)
    [ ] downgrade() asks for confirmation if destructive
    [ ] No DROP/TRUNCATE/DELETE without confirmation
    [ ] Tested on development environment
    [ ] Existing data will be preserved
    [ ] Backward compatibility maintained
    [ ] Performance impact considered
    [ ] Reviewed by team/database guardian

Affected Tables:
    - table_name_1: [what changes]
    - table_name_2: [what changes]
"""

import asyncio
import sys
import os

# Add parent directory to path so we can import backend modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

# Add backend directory to path for running inside container
sys.path.insert(0, '/app')

from sqlalchemy import text
from app.database.auth_db import auth_engine  # Or appropriate database engine


async def upgrade():
    """
    Apply migration changes

    CRITICAL RULES:
    - ✅ Use IF NOT EXISTS for CREATE operations
    - ✅ Check existence before ALTER TABLE ADD COLUMN
    - ✅ Preserve existing data
    - ✅ Use non-destructive operations only
    - ❌ NEVER DROP TABLE/DATABASE without explicit user permission
    - ❌ NEVER TRUNCATE or DELETE without WHERE clause
    """
    print("\n=== MIGRATION UP: [Description] ===\n")

    try:
        async with auth_engine.begin() as conn:

            # ================================================
            # EXAMPLE: Adding a new column
            # ================================================
            # check_column = text("""
            #     SELECT column_name
            #     FROM information_schema.columns
            #     WHERE table_name='users'
            #     AND column_name='new_column'
            #     AND table_schema='public'
            # """)
            # result = await conn.execute(check_column)
            # if result.fetchone():
            #     print("⊘ Column 'new_column' already exists, skipping...")
            # else:
            #     await conn.execute(text("""
            #         ALTER TABLE public.users
            #         ADD COLUMN new_column VARCHAR(255) NULL
            #     """))
            #     print("✓ Added column 'new_column' to users table")


            # ================================================
            # EXAMPLE: Creating a new table
            # ================================================
            # await conn.execute(text("""
            #     CREATE TABLE IF NOT EXISTS new_table (
            #         id SERIAL PRIMARY KEY,
            #         name VARCHAR(100) NOT NULL,
            #         created_at TIMESTAMP DEFAULT NOW()
            #     )
            # """))
            # print("✓ Created table 'new_table'")


            # ================================================
            # EXAMPLE: Adding an index
            # ================================================
            # check_index = text("""
            #     SELECT indexname
            #     FROM pg_indexes
            #     WHERE tablename='users'
            #     AND indexname='idx_users_email'
            # """)
            # result = await conn.execute(check_index)
            # if result.fetchone():
            #     print("⊘ Index 'idx_users_email' already exists, skipping...")
            # else:
            #     await conn.execute(text("""
            #         CREATE INDEX idx_users_email ON public.users(email)
            #     """))
            #     print("✓ Created index 'idx_users_email'")


            # ================================================
            # EXAMPLE: Adding a constraint
            # ================================================
            # check_constraint = text("""
            #     SELECT constraint_name
            #     FROM information_schema.table_constraints
            #     WHERE table_name='users'
            #     AND constraint_name='unique_username'
            # """)
            # result = await conn.execute(check_constraint)
            # if result.fetchone():
            #     print("⊘ Constraint 'unique_username' already exists, skipping...")
            # else:
            #     await conn.execute(text("""
            #         ALTER TABLE public.users
            #         ADD CONSTRAINT unique_username UNIQUE (username)
            #     """))
            #     print("✓ Added constraint 'unique_username'")


            # ================================================
            # EXAMPLE: Modifying column type (careful!)
            # ================================================
            # WARNING: Test this thoroughly! May fail if existing data incompatible
            # await conn.execute(text("""
            #     ALTER TABLE public.users
            #     ALTER COLUMN bio TYPE TEXT
            # """))
            # print("✓ Changed 'bio' column type to TEXT")


            # ================================================
            # EXAMPLE: Adding default value
            # ================================================
            # await conn.execute(text("""
            #     ALTER TABLE public.users
            #     ALTER COLUMN status SET DEFAULT 'active'
            # """))
            # print("✓ Set default value for 'status' column")


            # ================================================
            # EXAMPLE: Data migration (updating existing rows)
            # ================================================
            # WARNING: Use WHERE clause to target specific rows
            # result = await conn.execute(text("""
            #     UPDATE public.users
            #     SET status = 'active'
            #     WHERE status IS NULL
            # """))
            # print(f"✓ Updated {result.rowcount} users with NULL status")


            # ================================================
            # YOUR MIGRATION CODE HERE
            # ================================================

            # Remove the examples above and write your migration:
            # [Your SQL here]

            pass  # Remove this when you add your migration code

        print("\n=== MIGRATION COMPLETE ===\n")

        # ================================================
        # POST-MIGRATION VERIFICATION
        # ================================================
        # Optional: Verify migration succeeded
        # async with auth_engine.connect() as conn:
        #     result = await conn.execute(text("SELECT COUNT(*) FROM users"))
        #     count = result.scalar()
        #     print(f"Verification: users table has {count} rows")

    except Exception as e:
        print(f"\n✗ Migration failed: {e}\n")
        print("Rolling back transaction...")
        raise


async def downgrade():
    """
    Rollback migration changes

    CRITICAL: This function should:
    - ⚠️  Ask for user confirmation if destructive
    - 📋 Document what data will be lost
    - ✅ Be idempotent (check existence before dropping)
    - 🔒 Require explicit 'yes' for destructive operations
    """
    print("\n=== MIGRATION DOWN (ROLLBACK): [Description] ===\n")

    # ================================================
    # SAFETY CHECK: Confirm destructive operations
    # ================================================
    print("⚠️  WARNING: This rollback may DELETE DATA!")
    print("   - List what will be deleted here")
    print("   - Be specific about data loss")
    print()
    confirm = input("Type 'yes' to continue with rollback: ")

    if confirm.lower() != 'yes':
        print("Rollback cancelled by user.")
        return

    try:
        async with auth_engine.begin() as conn:

            # ================================================
            # EXAMPLE: Removing a constraint
            # ================================================
            # check_constraint = text("""
            #     SELECT constraint_name
            #     FROM information_schema.table_constraints
            #     WHERE table_name='users'
            #     AND constraint_name='unique_username'
            # """)
            # result = await conn.execute(check_constraint)
            # if not result.fetchone():
            #     print("⊘ Constraint 'unique_username' does not exist, skipping...")
            # else:
            #     await conn.execute(text("""
            #         ALTER TABLE public.users
            #         DROP CONSTRAINT unique_username
            #     """))
            #     print("✓ Removed constraint 'unique_username'")


            # ================================================
            # EXAMPLE: Removing an index
            # ================================================
            # check_index = text("""
            #     SELECT indexname
            #     FROM pg_indexes
            #     WHERE tablename='users'
            #     AND indexname='idx_users_email'
            # """)
            # result = await conn.execute(check_index)
            # if not result.fetchone():
            #     print("⊘ Index 'idx_users_email' does not exist, skipping...")
            # else:
            #     await conn.execute(text("DROP INDEX IF EXISTS idx_users_email"))
            #     print("✓ Removed index 'idx_users_email'")


            # ================================================
            # EXAMPLE: Removing a column (DATA LOSS!)
            # ================================================
            # check_column = text("""
            #     SELECT column_name
            #     FROM information_schema.columns
            #     WHERE table_name='users'
            #     AND column_name='new_column'
            #     AND table_schema='public'
            # """)
            # result = await conn.execute(check_column)
            # if not result.fetchone():
            #     print("⊘ Column 'new_column' does not exist, skipping...")
            # else:
            #     await conn.execute(text("""
            #         ALTER TABLE public.users
            #         DROP COLUMN new_column
            #     """))
            #     print("✓ Removed column 'new_column' from users table")


            # ================================================
            # EXAMPLE: Dropping a table (MAJOR DATA LOSS!)
            # ================================================
            # CRITICAL: Only drop tables created by this migration!
            # NEVER drop tables with existing production data!
            # await conn.execute(text("DROP TABLE IF EXISTS new_table"))
            # print("✓ Dropped table 'new_table'")


            # ================================================
            # YOUR ROLLBACK CODE HERE
            # ================================================

            # Remove the examples above and write your rollback:
            # [Your SQL here]

            pass  # Remove this when you add your rollback code

        print("\n=== ROLLBACK COMPLETE ===\n")

    except Exception as e:
        print(f"\n✗ Rollback failed: {e}\n")
        raise


# ================================================
# TESTING SECTION
# ================================================
async def test_migration():
    """
    Optional: Test function to verify migration worked correctly

    Run with: python migration.py test
    """
    print("\n=== TESTING MIGRATION ===\n")

    try:
        async with auth_engine.connect() as conn:
            # Example: Verify column exists
            # result = await conn.execute(text("""
            #     SELECT column_name, data_type, character_maximum_length
            #     FROM information_schema.columns
            #     WHERE table_name = 'users' AND column_name = 'new_column'
            # """))
            # row = result.fetchone()
            # if row:
            #     print(f"✓ Column exists: {row}")
            # else:
            #     print("✗ Column not found!")

            # Example: Verify table exists
            # result = await conn.execute(text("""
            #     SELECT table_name
            #     FROM information_schema.tables
            #     WHERE table_schema='public'
            #     AND table_name='new_table'
            # """))
            # if result.fetchone():
            #     print("✓ Table exists")
            # else:
            #     print("✗ Table not found!")

            # Example: Check data integrity
            # result = await conn.execute(text("SELECT COUNT(*) FROM users"))
            # count = result.scalar()
            # print(f"✓ Users table has {count} rows (data preserved)")

            pass

        print("\n=== TESTS PASSED ===\n")

    except Exception as e:
        print(f"\n✗ Tests failed: {e}\n")
        raise


# ================================================
# MAIN EXECUTION
# ================================================
if __name__ == "__main__":
    command = sys.argv[1] if len(sys.argv) > 1 else "up"

    if command == "up":
        print("Running migration UP (applying changes)...")
        asyncio.run(upgrade())
    elif command == "down":
        print("Running migration DOWN (rolling back)...")
        asyncio.run(downgrade())
    elif command == "test":
        print("Running migration tests...")
        asyncio.run(test_migration())
    else:
        print("""
Usage: python YYYYMMDD_HHMMSS_description.py [command]

Commands:
    up      Apply migration (default)
    down    Rollback migration (asks for confirmation)
    test    Test migration was applied correctly

Examples:
    python backend/migrations/20250103_143000_add_preferences.py up
    python backend/migrations/20250103_143000_add_preferences.py down
    python backend/migrations/20250103_143000_add_preferences.py test
        """)
        sys.exit(1)

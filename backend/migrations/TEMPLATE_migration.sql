-- ============================================
-- MIGRATION TEMPLATE
-- ============================================
--
-- INSTRUCTIONS:
-- 1. Copy this file to: YYYYMMDD_HHMMSS_description.sql
--    Example: 20250103_143000_add_user_preferences.sql
--
-- 2. Fill in the metadata below
--
-- 3. Write your UP migration (changes to apply)
--
-- 4. Write your DOWN migration (rollback instructions)
--
-- 5. Test in development environment first
--
-- 6. Review with @database-guardian before applying
--
-- ============================================

-- Migration: [Brief description of what this migration does]
-- Created: [YYYY-MM-DD HH:MM:SS]
-- Author: [Your name or tool name]
-- Ticket/Issue: [Reference to issue/ticket if applicable]

-- ============================================
-- PRE-FLIGHT CHECKLIST
-- ============================================
-- [ ] Migration file named with timestamp: YYYYMMDD_HHMMSS_description.sql
-- [ ] UP migration is idempotent (can run multiple times safely)
-- [ ] DOWN migration documented for rollback
-- [ ] No DROP/TRUNCATE/DELETE without WHERE clause
-- [ ] Tested on development environment
-- [ ] Existing data will be preserved
-- [ ] Backward compatibility maintained
-- [ ] Performance impact considered (indexes added if needed)
-- [ ] Reviewed by @database-guardian or team lead

-- ============================================
-- AFFECTED TABLES
-- ============================================
-- List all tables modified by this migration:
-- - table_name_1: [what changes]
-- - table_name_2: [what changes]

-- ============================================
-- UP MIGRATION (Apply Changes)
-- ============================================

-- Example: Adding a new column
-- ALTER TABLE users ADD COLUMN IF NOT EXISTS preferences JSONB DEFAULT '{}'::jsonb;

-- Example: Creating an index
-- CREATE INDEX IF NOT EXISTS idx_users_preferences ON users USING gin(preferences);

-- Example: Adding a constraint
-- ALTER TABLE users ADD CONSTRAINT check_email_format
--     CHECK (email ~* '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$');

-- Example: Creating a new table
-- CREATE TABLE IF NOT EXISTS user_preferences (
--     id SERIAL PRIMARY KEY,
--     user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
--     key VARCHAR(100) NOT NULL,
--     value TEXT,
--     created_at TIMESTAMP DEFAULT NOW(),
--     updated_at TIMESTAMP DEFAULT NOW(),
--     UNIQUE(user_id, key)
-- );

-- Example: Modifying column type (careful with data!)
-- ALTER TABLE users ALTER COLUMN bio TYPE TEXT;

-- Example: Setting default value
-- ALTER TABLE users ALTER COLUMN status SET DEFAULT 'active';

-- Your UP migration here:
-- [Write your migration SQL here]


-- ============================================
-- DOWN MIGRATION (Rollback)
-- ============================================
--
-- IMPORTANT: Keep these commented out by default
-- To rollback, uncomment and run these statements
--
-- Example rollback commands:

-- Remove constraint:
-- ALTER TABLE users DROP CONSTRAINT IF EXISTS check_email_format;

-- Remove index:
-- DROP INDEX IF EXISTS idx_users_preferences;

-- Remove column (CAUTION: Data loss!):
-- ALTER TABLE users DROP COLUMN IF EXISTS preferences;

-- Drop table (CAUTION: Data loss!):
-- DROP TABLE IF EXISTS user_preferences;

-- Your DOWN migration here (commented):
-- [Write your rollback SQL here]


-- ============================================
-- TESTING & VERIFICATION
-- ============================================

-- Verify column was added:
-- SELECT column_name, data_type, character_maximum_length, column_default, is_nullable
-- FROM information_schema.columns
-- WHERE table_name = 'users' AND column_name = 'preferences';

-- Verify index was created:
-- SELECT indexname, indexdef
-- FROM pg_indexes
-- WHERE tablename = 'users' AND indexname = 'idx_users_preferences';

-- Verify constraint was added:
-- SELECT constraint_name, constraint_type
-- FROM information_schema.table_constraints
-- WHERE table_name = 'users' AND constraint_name = 'check_email_format';

-- Verify table was created:
-- \dt user_preferences

-- Check table structure:
-- \d user_preferences

-- Test data integrity (example):
-- SELECT COUNT(*) FROM users WHERE preferences IS NOT NULL;

-- Your verification queries here:
-- [Write verification SQL here]


-- ============================================
-- PERFORMANCE IMPACT
-- ============================================

-- Document expected performance impact:
-- - Adding column: [Minimal/Moderate/High]
-- - Adding index: [Time estimate, table locks?]
-- - Data migration: [How many rows affected?]
-- - Downtime required: [Yes/No - duration]

-- If adding indexes, estimate build time:
-- SELECT pg_size_pretty(pg_total_relation_size('table_name'));


-- ============================================
-- ROLLBACK PROCEDURE
-- ============================================

-- If migration fails or needs to be rolled back:
-- 1. Stop the application (if necessary)
-- 2. Uncomment DOWN migration section above
-- 3. Run the rollback SQL
-- 4. Verify rollback with verification queries
-- 5. Document what went wrong in INCIDENTS.md
-- 6. Fix the migration and retry


-- ============================================
-- NOTES
-- ============================================

-- Additional notes, warnings, or context:
-- - [Any special considerations]
-- - [Dependencies on other migrations]
-- - [Known limitations]
-- - [Future work needed]

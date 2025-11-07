# Project Guidelines - Farout Development

## Database Operation Protocols

### CRITICAL: Data Preservation First

This project manages real user data for a Star Citizen organization management portal. ALL database operations must prioritize data preservation and follow proper migration practices.

---

## 🚫 NEVER ALLOWED (Without Explicit User Permission)

The following operations are **STRICTLY PROHIBITED** without user confirmation:

1. ❌ `DROP DATABASE` - Destroys entire database
2. ❌ `DROP TABLE` - Destroys table and all data (unless cleanup specifically requested)
3. ❌ `TRUNCATE TABLE` - Removes all rows from table
4. ❌ `DELETE FROM table` - Without WHERE clause (removes all data)
5. ❌ Any operation that destroys existing data

**Exception:** Only proceed with destructive operations if:
- User explicitly requests it
- User confirms after being warned about data loss
- Data backup/export option has been provided

---

## ✅ ALWAYS REQUIRED

All database modifications must follow these patterns:

### 1. Use Migrations for Schema Changes
- Create timestamped migration files
- Include UP and DOWN migrations
- Make migrations idempotent (can run multiple times)
- Test migrations before applying to production

### 2. Preserve Existing Data
- Use `ALTER TABLE` to modify existing tables
- Use `ADD COLUMN IF NOT EXISTS` for new columns
- Never drop and recreate tables with data
- Maintain backward compatibility

### 3. Safe Table Creation
- Use `CREATE TABLE IF NOT EXISTS`
- Check for existing tables before creating
- Document relationships and constraints

### 4. Targeted Data Operations
- Always use WHERE clauses in UPDATE/DELETE
- Test queries on development data first
- Log data modifications for audit trail

---

## Correct Implementation Patterns

### Adding New Columns

**✅ CORRECT:**
```sql
ALTER TABLE users ADD COLUMN IF NOT EXISTS rank_image VARCHAR(500);
ALTER TABLE users ADD COLUMN IF NOT EXISTS bio TEXT DEFAULT '';
```

**❌ WRONG:**
```sql
DROP TABLE users;
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50),
    rank_image VARCHAR(500)  -- Adding new column by recreating
);
```

### Modifying Column Types

**✅ CORRECT:**
```sql
ALTER TABLE users ALTER COLUMN email TYPE VARCHAR(255);
ALTER TABLE users ALTER COLUMN created_at SET DEFAULT NOW();
```

**❌ WRONG:**
```sql
DROP TABLE users;
CREATE TABLE users (
    email VARCHAR(255)  -- Changed from VARCHAR(100)
);
```

### Adding New Tables

**✅ CORRECT:**
```sql
CREATE TABLE IF NOT EXISTS blog_posts (
    id SERIAL PRIMARY KEY,
    title VARCHAR(200) NOT NULL,
    content TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT NOW()
);
```

**❌ WRONG:**
```sql
DROP DATABASE farout;
CREATE DATABASE farout;
CREATE TABLE blog_posts (...);
```

### Adding Indexes

**✅ CORRECT:**
```sql
CREATE INDEX IF NOT EXISTS idx_users_username ON users(username);
CREATE INDEX IF NOT EXISTS idx_posts_created ON blog_posts(created_at);
```

### Adding Constraints

**✅ CORRECT:**
```sql
ALTER TABLE users ADD CONSTRAINT unique_username UNIQUE (username);
ALTER TABLE blog_posts ADD CONSTRAINT fk_author
    FOREIGN KEY (author_id) REFERENCES users(id) ON DELETE CASCADE;
```

### Data Updates

**✅ CORRECT:**
```sql
UPDATE users SET role = 'admin' WHERE username = 'admin';
UPDATE blog_posts SET status = 'published' WHERE id = 123;
```

**❌ WRONG:**
```sql
DELETE FROM users;
INSERT INTO users VALUES (1, 'admin', 'admin');
```

---

## Migration File Structure

### Location
All migrations should be stored in: `backend/migrations/`

### Naming Convention
Format: `YYYYMMDD_HHMMSS_description.sql`

Examples:
- `20250103_143000_add_rank_image_column.sql`
- `20250103_150000_create_blog_posts_table.sql`
- `20250103_153000_add_user_indexes.sql`

### Template Structure

```sql
-- Migration: [Description of changes]
-- Created: YYYY-MM-DD HH:MM:SS
-- Author: [Name/Tool]

-- ============================================
-- UP MIGRATION (Apply changes)
-- ============================================

-- Add new column with default
ALTER TABLE users ADD COLUMN IF NOT EXISTS rank_image VARCHAR(500);

-- Create index for performance
CREATE INDEX IF NOT EXISTS idx_users_rank_image ON users(rank_image);

-- Add constraint
ALTER TABLE users ADD CONSTRAINT check_rank_image_url
    CHECK (rank_image IS NULL OR rank_image LIKE 'http%');

-- ============================================
-- DOWN MIGRATION (Rollback changes)
-- ============================================

-- To rollback, uncomment and run:
-- ALTER TABLE users DROP CONSTRAINT IF EXISTS check_rank_image_url;
-- DROP INDEX IF EXISTS idx_users_rank_image;
-- ALTER TABLE users DROP COLUMN IF EXISTS rank_image;

-- ============================================
-- TESTING
-- ============================================

-- Verify migration:
-- SELECT column_name, data_type, character_maximum_length
-- FROM information_schema.columns
-- WHERE table_name = 'users' AND column_name = 'rank_image';
```

### Migration Checklist

Before applying any migration:

- [ ] Migration file created with timestamp
- [ ] UP migration is idempotent (can run multiple times)
- [ ] DOWN migration documented (rollback plan)
- [ ] No destructive operations (DROP/TRUNCATE/DELETE without WHERE)
- [ ] Tested on development environment
- [ ] Existing data will be preserved
- [ ] Backward compatibility maintained
- [ ] Performance impact considered (indexes for new columns)

---

## Emergency Procedures

### If Database Needs Rebuild

**Only in genuinely corrupted/broken state:**

1. ⚠️ **ASK USER FIRST**
   ```
   CRITICAL: Database [name] needs to be dropped and recreated.
   This will DELETE ALL DATA including:
   - [X] user accounts
   - [X] blog posts
   - [X] organization data

   Proceed? (yes/no)
   ```

2. **Wait for Explicit Confirmation**
   - Do not proceed without clear "yes"
   - Provide alternative solutions if possible

3. **Document Data Loss**
   - List all tables affected
   - Estimate records that will be lost
   - Document recovery options

4. **Provide Backup Options**
   ```bash
   # Offer to backup first
   docker-compose exec db pg_dump -U farout farout > backup_$(date +%Y%m%d_%H%M%S).sql
   ```

### Recovery Options

**If destructive operation was accidentally run:**

1. Check for recent backups
2. Review Docker volume snapshots
3. Check git history for schema definitions
4. Document incident in INCIDENTS.md

---

## Agent-Specific Responsibilities

### Database Guardian (@database-guardian)
**Primary Responsibility:** Protect data integrity

- Review ALL database operations before execution
- Block any destructive operations without user confirmation
- Ensure migrations are non-destructive
- Verify schema changes preserve existing data
- Maintain migration history
- Monitor database health and performance

**Must Flag:**
- Any DROP/TRUNCATE/DELETE without WHERE
- Schema changes that could lose data
- Missing indexes on foreign keys
- Unsafe data type conversions

### Backend Builder (@backend-builder)
**Primary Responsibility:** Safe backend implementation

- Never write code that drops databases or tables
- Use migrations for all schema changes
- Test with existing data before deployment
- Preserve backward compatibility in APIs
- Use SQLAlchemy ORM for type safety
- Handle migration failures gracefully

**Must Follow:**
- Always use `IF NOT EXISTS` for CREATE operations
- Use `ALTER TABLE` for schema modifications
- Implement proper rollback logic
- Test migrations in development first

### Security Guardian (@security-guardian)
**Primary Responsibility:** Security and data protection

- Flag operations that could cause data loss
- Review migration safety and access controls
- Ensure no accidental data exposure
- Verify authentication on destructive endpoints
- Monitor for SQL injection vulnerabilities
- Check for sensitive data in logs

**Must Verify:**
- Migrations don't expose sensitive data
- Proper authentication on admin endpoints
- No SQL injection vulnerabilities
- Data encryption for sensitive fields

### Project Manager (@project-manager)
**Primary Responsibility:** Coordination and oversight

- Coordinate database changes across agents
- Require review of any DROP/TRUNCATE operations
- Ensure all agents follow these protocols
- Maintain changelog of database modifications
- Resolve conflicts between agent changes
- Escalate protocol violations

**Must Coordinate:**
- Cross-agent database changes
- Migration scheduling and testing
- Rollback procedures
- Documentation updates

---

## Testing Database Changes

### Pre-Deployment Testing

1. **Test in Development Environment**
   ```bash
   # Apply migration to dev database
   docker-compose exec db psql -U farout -d farout_dev -f migration.sql
   ```

2. **Verify Data Preservation**
   ```sql
   -- Check row counts before/after
   SELECT COUNT(*) FROM users;
   ```

3. **Test Rollback**
   ```sql
   -- Run DOWN migration
   -- Verify data restored
   ```

4. **Performance Testing**
   ```sql
   -- Check query performance
   EXPLAIN ANALYZE SELECT * FROM users WHERE rank_image IS NOT NULL;
   ```

### Validation Checklist

After applying migration:

```bash
# Should work (non-destructive):
ALTER TABLE users ADD COLUMN test_col VARCHAR(50);
SELECT test_col FROM users LIMIT 1;
ALTER TABLE users DROP COLUMN test_col;

# Should be blocked (destructive):
DROP TABLE users;  # ❌ Must ask user first
TRUNCATE TABLE users;  # ❌ Must ask user first
DELETE FROM users;  # ❌ Must ask user first (no WHERE clause)
```

---

## Code Review Requirements

### All Database Changes Must:

1. **Include Migration File**
   - Timestamped filename
   - UP and DOWN migrations
   - Testing queries

2. **Update Documentation**
   - Update CLAUDE.md if schema changes
   - Update API docs if endpoints change
   - Document in commit message

3. **Pass Safety Checks**
   - No DROP/TRUNCATE without permission
   - Data preservation verified
   - Rollback plan documented

4. **Get Approval**
   - Reviewed by @database-guardian
   - Tested in development
   - User approved if destructive

---

## Incident Response

### If Protocol Violation Occurs:

1. **Immediate Actions**
   - Stop deployment immediately
   - Assess data loss extent
   - Check for available backups

2. **Documentation**
   - Document what happened
   - Record lessons learned
   - Update guidelines if needed

3. **Recovery**
   - Restore from backup if available
   - Reconstruct data from logs
   - Communicate to stakeholders

4. **Prevention**
   - Update pre-flight checks
   - Add additional safeguards
   - Review agent protocols

---

## Additional Resources

### Useful Commands

```bash
# Backup database
docker-compose exec db pg_dump -U farout farout > backup.sql

# Restore database
docker-compose exec db psql -U farout farout < backup.sql

# View table structure
docker-compose exec db psql -U farout -d farout -c "\d users"

# List all tables
docker-compose exec db psql -U farout -d farout -c "\dt"

# Check table size
docker-compose exec db psql -U farout -d farout -c "SELECT pg_size_pretty(pg_total_relation_size('users'));"
```

### SQLAlchemy Migration Patterns

```python
# Safe column addition in models.py
class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(50), unique=True)
    rank_image: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)  # New column
```

---

## Summary

**Remember:** Data is irreplaceable. Always:
- ✅ Use migrations
- ✅ Preserve data
- ✅ Test changes
- ✅ Document everything
- ❌ Never DROP without permission

When in doubt, **ASK THE USER FIRST**.

# Database Operations Pre-Flight Checklist

Use this checklist before ANY database operation to ensure data safety and compliance with project protocols.

---

## ⚠️ STOP! Before You Proceed

### Question 1: Is this operation destructive?
Does your operation include any of the following?
- [ ] DROP DATABASE
- [ ] DROP TABLE
- [ ] TRUNCATE TABLE
- [ ] DELETE FROM table (without WHERE clause)
- [ ] Dropping columns that contain data
- [ ] Modifying column types that could lose data

**If YES to any above:** You MUST get explicit user permission first!

**Ask user:**
```
⚠️  CRITICAL: This operation will DELETE DATA:
   - [List specifically what will be deleted]
   - [Estimate how much data: X rows, Y tables, etc.]

   Proceed? (Requires explicit 'yes')
```

**Do NOT proceed without user typing 'yes'**

---

## 📋 Migration Checklist

### File Creation
- [ ] Migration file created with proper timestamp naming
  - Format: `YYYYMMDD_HHMMSS_description.sql` or `.py`
  - Example: `20250103_143000_add_user_preferences.sql`
- [ ] File placed in: `backend/migrations/`
- [ ] Template used (TEMPLATE_migration.sql or TEMPLATE_migration.py)

### Documentation
- [ ] Migration purpose clearly documented in file header
- [ ] Affected tables listed
- [ ] Author/creator documented
- [ ] Ticket/issue reference included (if applicable)

### Safety Requirements
- [ ] **CRITICAL:** No DROP/TRUNCATE/DELETE without WHERE clause
- [ ] **CRITICAL:** No destructive operations without user confirmation
- [ ] Uses IF NOT EXISTS for CREATE operations
- [ ] Checks existence before ALTER TABLE ADD COLUMN
- [ ] Uses ALTER TABLE instead of DROP/CREATE for schema changes
- [ ] Preserves all existing data
- [ ] Maintains backward compatibility

### Idempotency
- [ ] Migration can run multiple times safely
- [ ] Checks if changes already applied before applying them
- [ ] No errors if run twice on same database

### Rollback Plan
- [ ] DOWN migration documented
- [ ] Rollback steps tested (if possible)
- [ ] Data loss from rollback documented
- [ ] Confirmation required for destructive rollback

### Testing
- [ ] Tested in development environment first
- [ ] Verified data preservation after migration
- [ ] Verified rollback works correctly
- [ ] Performance impact assessed
- [ ] No unexpected side effects

### Performance Considerations
- [ ] Indexes created for new columns used in queries
- [ ] Foreign key indexes added
- [ ] Large data migrations broken into batches (if applicable)
- [ ] Table locks considered and minimized
- [ ] Estimated migration duration documented

### Review
- [ ] Code reviewed by team member or database guardian
- [ ] Migration follows PROJECT_GUIDELINES.md protocols
- [ ] Follows CLAUDE.md database safety section
- [ ] No security vulnerabilities introduced

---

## ✅ Correct Pattern Examples

### Adding a Column (SQL)
```sql
-- ✅ CORRECT
ALTER TABLE users ADD COLUMN IF NOT EXISTS rank_image VARCHAR(500);
```

### Adding a Column (Python)
```python
# ✅ CORRECT
check_query = text("""
    SELECT column_name
    FROM information_schema.columns
    WHERE table_name='users' AND column_name='rank_image'
""")
result = await conn.execute(check_query)
if not result.fetchone():
    await conn.execute(text("""
        ALTER TABLE users ADD COLUMN rank_image VARCHAR(500)
    """))
```

### Creating a Table (SQL)
```sql
-- ✅ CORRECT
CREATE TABLE IF NOT EXISTS blog_posts (
    id SERIAL PRIMARY KEY,
    title VARCHAR(200) NOT NULL,
    created_at TIMESTAMP DEFAULT NOW()
);
```

### Modifying Column Type (SQL)
```sql
-- ✅ CORRECT
ALTER TABLE users ALTER COLUMN bio TYPE TEXT;
```

### Adding an Index (SQL)
```sql
-- ✅ CORRECT
CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);
```

### Updating Data (SQL)
```sql
-- ✅ CORRECT (has WHERE clause)
UPDATE users SET status = 'active' WHERE status IS NULL;
```

---

## ❌ WRONG Pattern Examples

### DO NOT DO THESE

```sql
-- ❌ WRONG - Drops all data!
DROP TABLE users;
CREATE TABLE users (...);

-- ❌ WRONG - Destroys database!
DROP DATABASE farout;
CREATE DATABASE farout;

-- ❌ WRONG - Removes all rows!
TRUNCATE TABLE users;

-- ❌ WRONG - Deletes all data (no WHERE clause)!
DELETE FROM users;

-- ❌ WRONG - Creates duplicate if run twice
CREATE TABLE blog_posts (...);  -- Missing IF NOT EXISTS

-- ❌ WRONG - Errors if column exists
ALTER TABLE users ADD COLUMN rank_image VARCHAR(500);  -- Missing IF NOT EXISTS check
```

---

## 🔍 Verification Steps

After running migration, verify success:

### 1. Check Column Added
```sql
SELECT column_name, data_type, character_maximum_length, column_default
FROM information_schema.columns
WHERE table_name = 'users' AND column_name = 'new_column';
```

### 2. Check Table Created
```sql
SELECT table_name
FROM information_schema.tables
WHERE table_schema='public' AND table_name='new_table';
```

### 3. Check Index Created
```sql
SELECT indexname, indexdef
FROM pg_indexes
WHERE tablename='users' AND indexname='idx_users_email';
```

### 4. Check Data Preserved
```sql
SELECT COUNT(*) FROM users;  -- Compare before/after count
```

### 5. Check Constraint Added
```sql
SELECT constraint_name, constraint_type
FROM information_schema.table_constraints
WHERE table_name='users' AND constraint_name='unique_username';
```

---

## 🚨 Emergency Rollback Procedure

If migration fails or causes issues:

### Immediate Actions
1. **Stop** - Don't apply more changes
2. **Assess** - Determine what went wrong
3. **Backup** - If not already done:
   ```bash
   docker-compose exec db pg_dump -U farout farout > emergency_backup_$(date +%Y%m%d_%H%M%S).sql
   ```
4. **Rollback** - Run DOWN migration
5. **Verify** - Check data integrity after rollback
6. **Document** - Record what happened in incident log

### Rollback Commands

**For Python migrations:**
```bash
python backend/migrations/YYYYMMDD_HHMMSS_description.py down
```

**For SQL migrations:**
```bash
# Uncomment DOWN migration section in file, then:
docker-compose exec db psql -U farout -d farout -f backend/migrations/YYYYMMDD_HHMMSS_description.sql
```

### Post-Rollback
- [ ] Verify data restored to previous state
- [ ] Document incident in INCIDENTS.md
- [ ] Review what went wrong
- [ ] Fix migration script
- [ ] Test fix in development before retry

---

## 🛡️ Safety Protocols by Role

### Database Guardian Responsibilities
- Review ALL migrations before execution
- Block destructive operations without user OK
- Verify idempotency of migrations
- Ensure data preservation
- Approve migration execution

### Backend Builder Responsibilities
- Write migrations following templates
- Test in development first
- Document changes thoroughly
- Never write DROP DATABASE/TABLE code
- Use ALTER TABLE for schema changes

### Security Guardian Responsibilities
- Review for SQL injection risks
- Check for data exposure vulnerabilities
- Verify authentication on admin endpoints
- Ensure sensitive data handling

### Project Manager Responsibilities
- Coordinate migration timing
- Ensure all checklists completed
- Require reviews before execution
- Document migration history
- Resolve conflicts between changes

---

## 📊 Quick Decision Tree

```
Starting Database Operation
         |
         v
    Is it destructive? (DROP/TRUNCATE/DELETE without WHERE)
         |
    YES--+---> Ask user permission
         |            |
         |       User says NO --> STOP, find alternative
         |            |
         |       User says YES --> Document data loss, backup, proceed
         |
    NO---+---> Is it a schema change?
                |
           YES--+---> Use ALTER TABLE or CREATE IF NOT EXISTS
                |
                +---> Write migration file
                |
                +---> Make it idempotent (check existence)
                |
                +---> Test in development
                |
                +---> Get review
                |
                +---> Apply to production
                |
           NO---+---> Is it a data update?
                     |
                     +---> Use WHERE clause in UPDATE/DELETE
                     |
                     +---> Test query first
                     |
                     +---> Verify affected row count
                     |
                     +---> Apply changes
```

---

## 📝 Final Checklist Before Execution

Right before running migration in production:

- [ ] Backup created and verified
- [ ] All checklist items above completed
- [ ] Tested successfully in development
- [ ] Team/guardian reviewed and approved
- [ ] Rollback plan ready
- [ ] Monitoring in place to detect issues
- [ ] User notified if downtime expected
- [ ] Database connection available
- [ ] Sufficient disk space for operation
- [ ] Time window appropriate (not during peak usage)

**Only proceed if ALL items checked ✅**

---

## 🔗 Additional Resources

- **Full Protocols:** `PROJECT_GUIDELINES.md`
- **Quick Reference:** `CLAUDE.md` - Database Operation Safety Protocols section
- **Templates:** `backend/migrations/TEMPLATE_migration.sql` and `.py`
- **Examples:** `backend/migrations/20251103_123426_add_rank_image_to_users.py`

---

## ✨ Remember

**When in doubt, ASK THE USER!**

Data is irreplaceable. Better to ask than to destroy production data.

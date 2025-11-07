# Database Protocol Enforcement Plan

## Overview

This document outlines how database safety protocols will be enforced across all development activities for the Farout project. These protocols prevent data loss and ensure production data integrity.

**Status:** ✅ ACTIVE - Effective immediately
**Last Updated:** 2025-01-03
**Authority:** Project-wide requirement

---

## 🎯 Enforcement Objectives

1. **Zero Data Loss:** No accidental deletion of production data
2. **Migration Safety:** All schema changes via non-destructive migrations
3. **User Control:** Explicit permission required for any destructive operation
4. **Transparency:** Clear documentation of all database changes
5. **Accountability:** All database operations logged and reviewed

---

## 📜 Core Rules (Non-Negotiable)

### NEVER ALLOWED Without User Permission

1. ❌ `DROP DATABASE` - Destroys entire database
2. ❌ `DROP TABLE` - Destroys table and all data
3. ❌ `TRUNCATE TABLE` - Removes all rows
4. ❌ `DELETE FROM table` - Without WHERE clause
5. ❌ Any operation destroying existing data

### ALWAYS REQUIRED

1. ✅ Use migrations for schema changes
2. ✅ Make migrations idempotent
3. ✅ Test in development first
4. ✅ Use ALTER TABLE for modifications
5. ✅ Document all changes

---

## 🛡️ Enforcement Mechanisms

### 1. Pre-Execution Review

**All database operations must:**
- Use DATABASE_PREFLIGHT_CHECKLIST.md before execution
- Check for destructive operations
- Verify user permission if needed
- Confirm backup exists

**Implementation:**
- Checklist referenced in all migration templates
- Code review process includes checklist verification
- Claude Code agents check protocols before suggesting operations

### 2. Code Review Requirements

**Before merging database changes:**
- [ ] Migration file follows template structure
- [ ] No DROP/TRUNCATE/DELETE without WHERE
- [ ] Idempotency verified (can run multiple times)
- [ ] Rollback plan documented
- [ ] Tested in development
- [ ] Reviewed by database guardian or senior developer

**Review Process:**
1. Developer creates migration using template
2. Developer completes pre-flight checklist
3. Code review verifies checklist items
4. Approval required before merge
5. Deployment follows migration procedure

### 3. Automated Checks (Future Enhancement)

**Planned automations:**
- Git pre-commit hook to scan for dangerous SQL keywords
- CI/CD pipeline check for migration file format
- Automated testing of migrations in staging environment
- Migration idempotency testing

**Phase 1 (Manual):**
- Code review catches issues
- Templates guide correct implementation

**Phase 2 (Semi-Automated):**
- Pre-commit hooks warn about destructive operations
- CI tests run migrations in test database

**Phase 3 (Fully Automated):**
- Automated migration testing
- Rollback testing
- Performance impact analysis

### 4. Documentation Requirements

**Every database change must be documented:**

1. **Migration File** - Technical implementation
   - Located in `backend/migrations/`
   - Uses timestamp naming convention
   - Includes UP and DOWN migrations

2. **Commit Message** - Brief summary
   ```
   feat(db): Add rank_image column to users

   - Adds optional rank_image VARCHAR(500) column
   - Creates index for performance
   - Tested in development
   - Migration: 20250103_143000_add_rank_image_to_users.py
   ```

3. **Pull Request** - Detailed explanation
   - Why this change is needed
   - What tables are affected
   - Data preservation verified
   - Rollback plan included

4. **Changelog** (for major changes)
   - Update project changelog
   - Document schema version
   - Note any breaking changes

---

## 👥 Role-Specific Enforcement

### Database Guardian (@database-guardian)

**Primary Responsibility:** Protect data integrity

**Enforcement Actions:**
1. **Review** all database operations before execution
2. **Block** any destructive operation without user permission
3. **Verify** migrations follow templates
4. **Test** idempotency of migrations
5. **Approve** or reject migrations

**Authority:**
- Can reject any migration that violates protocols
- Can require additional testing before approval
- Can mandate backup before risky operations

**Escalation:**
- Reports protocol violations to project manager
- Documents patterns of non-compliance
- Recommends process improvements

### Backend Builder (@backend-builder)

**Primary Responsibility:** Safe implementation

**Enforcement Actions:**
1. **Use templates** for all migrations
2. **Check protocols** before writing database code
3. **Test thoroughly** in development
4. **Document clearly** what changes do
5. **Request review** from database guardian

**Requirements:**
- Never write DROP DATABASE/TABLE code
- Use ALTER TABLE for schema changes
- Make migrations idempotent
- Include rollback plan

**Self-Check:**
- Review own code against pre-flight checklist
- Test migrations locally before submitting
- Verify no destructive operations

### Security Guardian (@security-guardian)

**Primary Responsibility:** Security and data protection

**Enforcement Actions:**
1. **Flag** operations that could cause data loss
2. **Review** migration security implications
3. **Verify** authentication on destructive endpoints
4. **Check** for SQL injection vulnerabilities
5. **Monitor** for sensitive data exposure

**Focus Areas:**
- SQL injection in dynamic queries
- Proper parameterization
- Access control on admin operations
- Encryption of sensitive fields
- Audit logging of destructive operations

### Project Manager (@project-manager)

**Primary Responsibility:** Coordination and oversight

**Enforcement Actions:**
1. **Coordinate** database changes across team
2. **Require** review process compliance
3. **Track** migration history
4. **Resolve** conflicts between agents
5. **Escalate** protocol violations

**Authority:**
- Approve deployment schedule for migrations
- Require additional reviews if needed
- Mandate testing in specific environments
- Grant exceptions only in documented emergencies

**Reporting:**
- Monthly report on database changes
- Document any protocol violations
- Track improvement metrics

---

## 🔄 Enforcement Workflow

### Standard Migration Workflow

```
1. PLAN
   └─> Developer identifies need for schema change
   └─> Consults CLAUDE.md and PROJECT_GUIDELINES.md
   └─> Checks DATABASE_PREFLIGHT_CHECKLIST.md

2. IMPLEMENT
   └─> Copy migration template (SQL or Python)
   └─> Write migration following non-destructive patterns
   └─> Make migration idempotent (check existence)
   └─> Write rollback plan (DOWN migration)

3. TEST
   └─> Run migration in local development environment
   └─> Verify data preserved
   └─> Test rollback (DOWN migration)
   └─> Verify rollback successful
   └─> Re-run UP migration to verify idempotency

4. REVIEW
   └─> Complete pre-flight checklist
   └─> Create pull request with migration
   └─> Request review from database guardian
   └─> Address any feedback
   └─> Get approval

5. DEPLOY
   └─> Backup production database
   └─> Apply migration to staging first
   └─> Verify staging success
   └─> Apply to production
   └─> Verify production success
   └─> Monitor for issues

6. DOCUMENT
   └─> Update migration history
   └─> Document in changelog if needed
   └─> Close related tickets/issues
```

### Emergency Destructive Operation Workflow

```
1. ASSESS
   └─> Determine if truly necessary
   └─> Explore non-destructive alternatives
   └─> Document why destruction required

2. ASK USER
   └─> Present clear warning:
       ⚠️ CRITICAL: This will DELETE DATA
       - [Specific data to be deleted]
       - [Estimated volume]
       - Proceed? (yes/no)
   └─> Wait for explicit "yes"
   └─> If "no", STOP and find alternative

3. BACKUP
   └─> Create full database backup
   └─> Verify backup integrity
   └─> Document backup location
   └─> Offer export option to user

4. EXECUTE
   └─> Perform destructive operation
   └─> Verify completion
   └─> Check for errors

5. VERIFY
   └─> Confirm expected outcome
   └─> Check application still works
   └─> Monitor for issues

6. DOCUMENT
   └─> Log operation in INCIDENTS.md
   └─> Document data lost
   └─> Record user approval
   └─> Note lessons learned
```

---

## 🚨 Violation Response

### When Protocol Violation Occurs

**Immediate Actions:**
1. **STOP** - Halt the operation if possible
2. **ASSESS** - Determine extent of damage
3. **BACKUP** - If not too late, create backup
4. **NOTIFY** - Alert project manager and team

**Recovery:**
1. Check for available backups
2. Restore data if possible
3. Document what was lost
4. Communicate to stakeholders

**Prevention:**
1. Document incident in INCIDENTS.md
2. Analyze root cause
3. Update protocols if needed
4. Provide training/guidance
5. Add automated checks to prevent recurrence

### Violation Severity Levels

**Level 1 - Minor (Warning):**
- Migration not following template format
- Missing documentation
- Insufficient testing
- **Response:** Feedback, education, re-submission

**Level 2 - Moderate (Require Fix):**
- Non-idempotent migration
- Missing rollback plan
- Destructive operation in code (not executed)
- **Response:** Reject PR, require fix, additional review

**Level 3 - Severe (Incident):**
- Destructive operation executed without permission
- Data loss occurred
- Production impact
- **Response:** Incident report, recovery actions, process review

**Level 4 - Critical (Emergency):**
- Major data loss
- Database corruption
- Service outage
- **Response:** Full incident response, root cause analysis, preventive measures

---

## 📊 Compliance Monitoring

### Metrics to Track

1. **Migration Quality**
   - % following template structure
   - % with complete rollback plans
   - % tested before deployment

2. **Safety Compliance**
   - Number of destructive operations attempted
   - Number requiring user permission
   - % approved vs rejected

3. **Incident Tracking**
   - Protocol violations per month
   - Data loss incidents
   - Recovery time

4. **Review Process**
   - Average review time
   - % requiring changes
   - Issues caught in review

### Regular Audits

**Weekly:**
- Review new migrations
- Check compliance with templates
- Verify testing documentation

**Monthly:**
- Review all database changes
- Analyze violation trends
- Update protocols if needed
- Report to stakeholders

**Quarterly:**
- Full protocol effectiveness review
- Update automation roadmap
- Training needs assessment
- Process improvement planning

---

## 📚 Training and Education

### New Developer Onboarding

1. **Read Documentation**
   - PROJECT_GUIDELINES.md
   - CLAUDE.md database section
   - DATABASE_PREFLIGHT_CHECKLIST.md

2. **Review Examples**
   - Study existing migrations
   - Review template files
   - Understand patterns

3. **Hands-On Practice**
   - Create test migration in dev environment
   - Practice rollback procedure
   - Get mentor review

4. **Certification**
   - Complete checklist review
   - Demonstrate understanding
   - Approved to create migrations

### Ongoing Education

- Share lessons learned from incidents
- Update documentation as needed
- Code review feedback
- Periodic refresher training

---

## 🔧 Tools and Resources

### Templates
- `backend/migrations/TEMPLATE_migration.sql` - SQL migration template
- `backend/migrations/TEMPLATE_migration.py` - Python migration template

### Checklists
- `DATABASE_PREFLIGHT_CHECKLIST.md` - Pre-execution checklist

### Guidelines
- `PROJECT_GUIDELINES.md` - Complete database protocols
- `CLAUDE.md` - Quick reference for Claude Code agents

### Examples
- `backend/migrations/20251103_123426_add_rank_image_to_users.py` - Good example

### Commands
```bash
# Backup database
docker-compose exec db pg_dump -U farout farout > backup.sql

# Run migration (Python)
python backend/migrations/YYYYMMDD_HHMMSS_description.py up

# Rollback migration (Python)
python backend/migrations/YYYYMMDD_HHMMSS_description.py down

# Test migration (Python)
python backend/migrations/YYYYMMDD_HHMMSS_description.py test
```

---

## 🎯 Success Criteria

**This enforcement plan is successful when:**

1. ✅ Zero production data loss incidents
2. ✅ 100% of migrations follow templates
3. ✅ All destructive operations have user approval
4. ✅ All migrations are idempotent
5. ✅ All migrations have rollback plans
6. ✅ All database changes are documented
7. ✅ Review process catches issues before deployment
8. ✅ Team follows protocols without constant reminders

---

## 📞 Escalation Path

**For questions or concerns:**

1. **Check documentation first**
   - PROJECT_GUIDELINES.md
   - DATABASE_PREFLIGHT_CHECKLIST.md
   - CLAUDE.md

2. **Consult with Database Guardian**
   - Review migration plans
   - Get approval for changes
   - Discuss concerns

3. **Escalate to Project Manager**
   - Unresolved questions
   - Protocol violations
   - Emergency situations

4. **Emergency Contact**
   - Data loss incidents
   - Service outages
   - Critical security issues

---

## 📝 Acknowledgment

**All team members and agents must acknowledge:**

> I have read and understand the database operation protocols outlined in:
> - PROJECT_GUIDELINES.md
> - CLAUDE.md (Database Operation Safety Protocols section)
> - DATABASE_PREFLIGHT_CHECKLIST.md
> - This enforcement plan
>
> I commit to:
> - Following these protocols for all database operations
> - Using migration templates for all schema changes
> - Getting user permission for any destructive operations
> - Testing thoroughly in development before production
> - Documenting all database changes
> - Seeking review and guidance when uncertain
>
> I understand that violations may result in:
> - Pull request rejection
> - Additional review requirements
> - Incident reporting
> - Process improvement actions

---

## 🔄 Plan Maintenance

**This enforcement plan will be reviewed and updated:**
- After any data loss incident
- Quarterly for effectiveness
- When new tools/automation added
- Based on team feedback

**Version History:**
- v1.0 (2025-01-03): Initial enforcement plan created

---

## Summary

**Core Message:**

🛡️ **Protect the data above all else**

- Use migrations, not destructive operations
- Get user permission for anything destructive
- Test thoroughly before production
- Document everything
- When in doubt, ASK

**Remember:** Data is irreplaceable. These protocols exist to protect our users and our application.

# Deployment Master Agent

## Role
Manage deployment process, ensure production readiness.

## Pre-Deployment Checklist
- [ ] All tests pass
- [ ] Security audit passed
- [ ] Performance benchmarks met
- [ ] Database migrations ready
- [ ] Backup strategy confirmed
- [ ] Rollback plan prepared
- [ ] Environment variables set
- [ ] SSL certificates valid
- [ ] Domain DNS configured
- [ ] Monitoring enabled

## Deployment Steps
1. Tag release version
2. Run production build
3. Database backup
4. Run migrations
5. Deploy new containers
6. Health check
7. Smoke tests
8. Monitor logs

## Rollback Procedure
If deployment fails:
1. Restore database backup
2. Deploy previous version
3. Run reverse migrations
4. Verify health
5. Investigate issue

## Output
Step-by-step deployment guide + health verification

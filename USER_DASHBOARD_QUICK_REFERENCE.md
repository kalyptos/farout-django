# User Dashboard Quick Reference

## Access the Dashboard

**URL:** `http://YOUR_SERVER_IP:3000/user`

**Requirements:** Must be logged in (redirects to `/login` if not authenticated)

---

## What Users See

### All Users (Members & Admins)
1. **Profile Card**
   - Discord avatar
   - Username
   - Email
   - Role badge (Admin/Member)
   - Member since date
   - Last login timestamp

2. **Rank Card**
   - Current rank
   - Rank badge image (if set by admin)

3. **Stats Card** (if member data exists)
   - Missions completed count
   - Trainings completed count
   - Member since date

4. **Bio Card** (if bio exists)
   - Personal bio text

5. **Quick Actions**
   - Change Password link
   - View Organization Members link
   - **Admin Panel link** (admins only)

---

## How to Get There

### Method 1: Direct Navigation
- Navigate to: `http://YOUR_SERVER_IP:3000/user`
- If not logged in → redirects to `/login`

### Method 2: After Discord Login
1. Click "Login with Discord" on `/login` page
2. Authorize on Discord
3. Automatically redirected to `/user`

### Method 3: After Admin Login
1. Enter credentials on `/login` page
2. If admin → redirects to `/admin`
3. If member → redirects to `/user`

---

## File Locations

### Created Files
```
/frontend/app/types/user.ts              - TypeScript types
/frontend/app/composables/useUserProfile.ts  - API composable
/frontend/app/pages/user.vue             - Dashboard page
```

### Modified Files
```
/frontend/app/pages/auth/discord/callback.vue  - Discord redirect
/frontend/app/middleware/admin.ts              - Admin redirect
```

---

## Backend API

**Endpoint:** `GET /api/auth/user/me`

**Returns:**
```json
{
  "username": "string",
  "discord_id": "string | null",
  "email": "string",
  "role": "admin" | "member",
  "rank": "string",
  "rank_image": "string | null",
  "created_at": "ISO timestamp",
  "last_login": "ISO timestamp | null",
  "member_id": "number | null",
  "member_data": {
    "display_name": "string",
    "bio": "string | null",
    "avatar_url": "string | null",
    "missions_completed": [],
    "trainings_completed": [],
    "stats": {},
    "member_since": "ISO timestamp"
  } | null
}
```

---

## Responsive Breakpoints

- **Mobile (< 768px):** Single column, vertical layout
- **Tablet (768px - 1024px):** 2-column grid
- **Desktop (1024px+):** 3-column grid

---

## Troubleshooting

### Issue: Redirects to /login
**Cause:** Not authenticated or session expired
**Fix:** Log in again via Discord or admin credentials

### Issue: No stats showing
**Cause:** User doesn't have `member_data` (admin-only accounts)
**Fix:** Normal behavior - stats only show for Discord users with member records

### Issue: Avatar not loading
**Cause:** Invalid avatar URL or network issue
**Fix:** Falls back to default SVG avatar automatically

### Issue: Can't access /admin
**Cause:** Non-admin user trying to access admin panel
**Fix:** Normal behavior - redirects to `/user` dashboard

---

## Key Features

- **Protected Route:** Requires authentication
- **Auto-refresh:** Fetches latest data on page load
- **Error Handling:** Shows retry button on API failures
- **Responsive Design:** Works on all screen sizes
- **Role-based UI:** Admin panel link only for admins
- **Fallback Avatar:** Default SVG if Discord avatar missing

---

## Related Pages

- `/login` - Login page
- `/members` - Organization members showcase (public)
- `/admin` - Admin panel (admins only)
- `/change-password` - Password change page
- `/auth/discord/callback` - Discord OAuth callback

---

## Testing Commands

```bash
# Check container status
docker-compose ps farout_frontend

# View logs
docker-compose logs --tail=50 farout_frontend

# Restart frontend
docker-compose restart farout_frontend

# Rebuild after code changes
docker-compose build farout_frontend && docker-compose up -d farout_frontend
```

---

## Important Notes

1. **Read-Only Dashboard:** This page displays data only. Editing requires separate features.
2. **Session Persistence:** Uses JWT cookies for authentication.
3. **Auto-Redirect:** Protected by `auth` middleware.
4. **Admin Detection:** Checks `role === 'admin'` for conditional features.

---

## Next Steps

After viewing dashboard, users can:
- Change password via link
- View organization members
- Access admin panel (if admin)
- Navigate to other public pages

---

**Documentation:** See `/home/ubuntu/docker/farout/FRONTEND_USER_DASHBOARD_COMPLETE.md` for full implementation details.

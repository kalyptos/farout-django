# Admin Portal Testing Guide

## Prerequisites

1. **Backend Running:** Ensure farout_backend container is healthy
2. **Database Running:** Ensure db container is healthy
3. **Frontend Running:** Ensure farout_frontend container is healthy
4. **Admin Account:** Have admin credentials ready (default: admin / Admin123!)

---

## Testing Steps

### 1. Admin Dashboard (http://localhost:3000/admin)

#### Authentication Test
1. Open http://localhost:3000/login
2. Login with admin credentials:
   - Username: `admin`
   - Password: `Admin123!`
3. Should redirect to `/admin` dashboard

#### Dashboard Display Test
1. Verify page header shows "Admin Dashboard"
2. Verify welcome message shows: "Welcome, admin!"
3. Check all 3 management cards are displayed:
   - User Management (pink gradient icon)
   - Blog Posts (purple gradient icon)
   - Members (cyan gradient icon)

#### Statistics Test
1. Wait for stats to load (loading spinner should appear)
2. Verify User Management card shows:
   - Total Users count (number)
   - Admins count (number)
3. Verify Blog Posts card shows:
   - Total Posts count (number)
   - Published count (number)
4. Check stats are numeric and reasonable

#### Navigation Test
1. Hover over each card - should lift up and show blue border
2. Click "User Management" card → should navigate to `/admin/users`
3. Go back, click "Blog Posts" card → should navigate to `/admin/blog`
4. Go back, click "Members" card → should navigate to `/members`

---

### 2. User Management (http://localhost:3000/admin/users)

#### Page Load Test
1. Navigate to `/admin/users`
2. Verify page header shows "User Management"
3. Verify breadcrumb trail: Home > Admin > Users
4. Wait for user table to load
5. Should see list of users (at least the admin user)

#### Search Functionality Test
1. **Search by username:**
   - Type "admin" in search box
   - Wait 500ms (debounce delay)
   - Should filter to show only admin user
   - Click X button to clear search

2. **Search by email:**
   - If users have emails, search by email
   - Should filter results
   - Clear search

3. **Search by Discord ID:**
   - If Discord users exist, search by Discord ID
   - Should filter results
   - Clear search

4. **Search with no results:**
   - Type "nonexistentuser123"
   - Should show empty state: "No users found"
   - Should show "Clear Filters" button
   - Click to reset

#### Filter Functionality Test
1. **Filter by Admin:**
   - Select "Admins Only" from dropdown
   - Should show only admin users
   - Verify role badges all show "ADMIN"

2. **Filter by Member:**
   - Select "Members Only" from dropdown
   - Should show only member users
   - Verify role badges all show "MEMBER"

3. **Combined Search + Filter:**
   - Enter search term
   - Select role filter
   - Should apply both filters
   - Click "Reset" button
   - Both filters should clear

#### Table Display Test
1. **Verify all columns:**
   - ID (numeric)
   - Username (with user icon)
   - Email (or "-" if none)
   - Role (colored badge with icon)
   - Rank (with image if available)
   - Discord (Discord icon + ID, or "Local" badge)
   - Status (Active/Inactive badge)
   - Joined (formatted date)
   - Actions (3 buttons)

2. **Hover effects:**
   - Hover over table rows → should highlight row
   - Hover over action buttons → should show darker background

3. **Responsive test:**
   - Resize browser to tablet width (768px-1200px)
   - Discord column should hide
   - Resize to mobile (<768px)
   - ID, Discord, and Joined columns should hide

#### Change Role Test
1. **Find a member user** (not yourself)
2. Click the blue shield icon (Change Role button)
3. **Modal should open:**
   - Title: "Change User Role"
   - Shows username
   - Shows current role badge
   - Dropdown to select new role

4. **Change member to admin:**
   - Select "Admin" from dropdown
   - Click "Confirm" button
   - Should show loading spinner on button
   - Modal should close
   - Toast should appear: "Role updated successfully" (green)
   - Table should refresh
   - User's role badge should now show "ADMIN"

5. **Change back to member:**
   - Repeat process, select "Member"
   - Verify role updates correctly

6. **Try to change own role (should fail):**
   - Find your own user (the admin you're logged in as)
   - Click Change Role button
   - Try to change to "Member"
   - Click Confirm
   - Should show error toast: "Cannot change your own role" (red)
   - Your role should NOT change

#### Edit Rank Test
1. **Find any user**
2. Click the yellow medal icon (Edit Rank button)
3. **Modal should open:**
   - Title: "Edit User Rank"
   - Shows username
   - Input for rank name (current value pre-filled)
   - Input for rank image URL (current value if exists)

4. **Update rank name only:**
   - Change rank to "Captain"
   - Leave image URL blank
   - Click "Save" button
   - Should show loading spinner
   - Modal should close
   - Toast should appear: "Rank updated successfully" (green)
   - Table should refresh
   - User's rank should now show "Captain"

5. **Update rank with image:**
   - Click Edit Rank again
   - Change rank to "Commander"
   - Enter image URL: `https://via.placeholder.com/50/007bff/ffffff?text=CMD`
   - Should see image preview below
   - Click "Save"
   - Toast should appear
   - Table should show "Commander" with badge image

6. **Test broken image URL:**
   - Click Edit Rank
   - Enter invalid URL: `https://invalid.example/broken.png`
   - Preview should show placeholder error image
   - Save anyway (backend will accept it)
   - In table, broken images should hide gracefully

7. **Test validation:**
   - Click Edit Rank
   - Clear rank name completely
   - "Save" button should be disabled (gray)
   - Cannot save without rank name

#### Delete User Test
1. **Find a non-admin test user** (NOT yourself)
2. Click the red trash icon (Delete User button)
3. **Confirmation modal should open:**
   - Red/danger styling
   - Warning icon
   - Message: "Are you sure you want to delete [username]?"
   - Explains soft delete behavior
   - Cancel and Delete buttons

4. **Cancel deletion:**
   - Click "Cancel" button
   - Modal should close
   - User should remain active

5. **Confirm deletion:**
   - Click Delete button again
   - Click "Delete User" button (red)
   - Should show loading spinner
   - Modal should close
   - Toast should appear: "User deleted successfully" (green)
   - Table should refresh
   - User should now have "INACTIVE" status badge
   - Delete button should be disabled (grayed out)

6. **Try to delete yourself (should fail):**
   - Find your own user
   - Click Delete button
   - Click "Delete User" in modal
   - Should show error toast: "Cannot delete your own account" (red)
   - You should remain active

7. **Verify deleted user cannot login:**
   - Logout
   - Try to login with deleted user's credentials
   - Should fail with "Account is inactive" error

#### Pagination Test
1. **If database has more than 20 users:**
   - Should see pagination controls at bottom
   - Page info shows: "Page 1 of X (Y users)"
   
2. **Next/Previous buttons:**
   - Click "Next" button → should go to page 2
   - Table should show users 21-40
   - URL should NOT change (client-side pagination)
   - Click "Previous" button → back to page 1
   - At page 1, "Previous" should be disabled
   - At last page, "Next" should be disabled

3. **Page number buttons:**
   - Should see up to 5 page numbers
   - Current page highlighted in blue
   - Click page 3 → jumps to page 3
   - Page numbers should update smartly

4. **Pagination with filters:**
   - Apply search filter (reduces total results)
   - Pagination should update to reflect filtered total
   - Clear filters → pagination resets

#### Toast Notification Test
1. **Success toast:**
   - Perform any successful action
   - Green toast should appear bottom-right
   - Check icon (✓) on left
   - Message text in center
   - X button on right
   - Should auto-dismiss after 4 seconds

2. **Error toast:**
   - Perform action that fails (try to change own role)
   - Red toast should appear
   - Exclamation icon (!) on left
   - Error message text
   - X button on right
   - Should auto-dismiss after 4 seconds

3. **Manual close:**
   - Trigger a toast
   - Click X button before auto-dismiss
   - Toast should close immediately

4. **Multiple toasts:**
   - Trigger action quickly
   - Only one toast should show at a time
   - New toast replaces old toast

#### Loading States Test
1. **Table loading:**
   - Refresh page
   - Should see spinner with "Loading users..." message
   - No table shown until data loads

2. **Action loading:**
   - Click any action button
   - Button should show spinner
   - Button should be disabled during load
   - Cannot click again until complete

3. **Modal loading:**
   - Open any modal
   - Click confirm button
   - Button shows spinner
   - Button is disabled
   - Modal does not close until complete

#### Error Handling Test
1. **Network error:**
   - Stop backend container: `docker-compose stop farout_backend`
   - Try to load users page
   - Should show error state with retry button
   - Click retry → still fails
   - Restart backend: `docker-compose start farout_backend`
   - Click retry → should load successfully

2. **403 Forbidden:**
   - Login as regular member (not admin)
   - Try to access `/admin/users`
   - Should redirect to `/user` dashboard

3. **401 Unauthorized:**
   - Logout
   - Try to access `/admin/users` directly
   - Should redirect to `/login`

---

## Expected Results Summary

### Admin Dashboard
- ✅ Protected by admin middleware
- ✅ Shows personalized welcome message
- ✅ Displays real-time statistics
- ✅ All cards link to correct pages
- ✅ Responsive on all screen sizes
- ✅ No console errors

### User Management
- ✅ Paginated user list (20 per page)
- ✅ Search works across username/email/Discord ID
- ✅ Role filter works (admin/member/all)
- ✅ Reset clears all filters
- ✅ Change role works (prevents self-demotion)
- ✅ Edit rank works (with image support)
- ✅ Delete user works (soft delete, prevents self-deletion)
- ✅ All modals open/close correctly
- ✅ Toast notifications show for all actions
- ✅ Loading states prevent double-clicks
- ✅ Error handling works gracefully
- ✅ Responsive design adapts to screen size
- ✅ No console errors

---

## Common Issues & Solutions

### Issue: Admin dashboard shows 0 users/posts
**Solution:** Check backend is running and accessible. Check browser console for API errors.

### Issue: Search doesn't work
**Solution:** Wait 500ms after typing (debounce delay). Check search term matches exactly (case-sensitive).

### Issue: Modal doesn't close after action
**Solution:** Check browser console for errors. Ensure backend returns successful response.

### Issue: Toast doesn't appear
**Solution:** Check toast HTML is rendered (inspect page). May be hidden off-screen on mobile.

### Issue: Pagination shows incorrect page count
**Solution:** Check backend response includes correct `total` and `pages` values.

### Issue: Images don't load
**Solution:** Check image URLs are accessible. CORS may block external images. Use placeholder or base64.

### Issue: Styles look broken
**Solution:** Clear browser cache. Rebuild frontend container. Check SCSS compilation succeeded.

---

## Performance Benchmarks

- **Initial page load:** < 2 seconds
- **Table load:** < 1 second (for 20 users)
- **Search filter:** < 500ms (plus 500ms debounce)
- **Role change:** < 500ms
- **Rank update:** < 500ms
- **User delete:** < 500ms
- **Pagination:** < 500ms

If any operation takes longer, check:
1. Network latency (backend response time)
2. Database query performance
3. Frontend re-render performance

---

## Browser Compatibility

Tested and working on:
- ✅ Chrome 120+
- ✅ Firefox 120+
- ✅ Safari 17+
- ✅ Edge 120+

May not work on:
- ❌ Internet Explorer (not supported by Nuxt 4)
- ❌ Chrome < 100 (missing modern JS features)

---

## Accessibility Testing

1. **Keyboard navigation:**
   - Tab through all interactive elements
   - Enter/Space to click buttons
   - Escape to close modals

2. **Screen reader:**
   - All images have alt text
   - All buttons have labels
   - All form inputs have labels
   - Status messages announced

3. **Color contrast:**
   - Text meets WCAG AA standard
   - Color not sole indicator of status
   - Icons supplement color coding

---

## Security Testing

1. **Admin-only access:**
   - Non-admin cannot access /admin
   - Non-admin cannot access /admin/users
   - Both redirect to appropriate page

2. **Self-protection:**
   - Admin cannot change own role
   - Admin cannot delete self
   - Error messages shown, no data change

3. **XSS prevention:**
   - User input sanitized
   - No script injection in username/email
   - Images validated as URLs

4. **CSRF protection:**
   - JWT token in HTTP-only cookie
   - Token sent with all requests
   - Backend validates token

---

## Next Steps After Testing

If all tests pass:
1. ✅ Mark Phase 5 as complete
2. ✅ Commit changes to git
3. ✅ Document any issues found
4. ✅ Plan next phase (if any)

If tests fail:
1. ❌ Document exact failure scenario
2. ❌ Check browser console for errors
3. ❌ Check backend logs for errors
4. ❌ Provide reproduction steps
5. ❌ Request fixes

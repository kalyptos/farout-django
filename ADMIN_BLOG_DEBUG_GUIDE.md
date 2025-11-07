# Admin Blog Debug Guide

## Issue: Loading Loop After CSS Changes

The admin blog page `/admin/blog/` sometimes gets stuck in an endless preloader loop.

## Solutions Implemented:

### 1. **Added Debug Console Logging**
Open your browser console (F12) and look for these messages:
```
[Admin Blog] Component mounted, loading posts...
[Admin Blog] Starting to load posts...
[Admin Blog] Calling fetchAllBlogPosts...
[Admin Blog] Response received: {...}
[Admin Blog] Posts loaded successfully: 9
[Admin Blog] Setting loading to false
```

### 2. **Added 10-Second Timeout Safety**
If the API takes longer than 10 seconds, loading will automatically stop with an error message.

### 3. **Improved Error Handling**
All errors are now caught and displayed with details.

## How to Debug:

1. **Open Browser Console** (F12 → Console tab)
2. **Visit:** http://51.68.46.56:3000/admin/blog/
3. **Check for logs starting with `[Admin Blog]`**
4. **Look for errors** (red text in console)

## Common Issues:

### Issue 1: Network Error
**Symptoms:** Console shows network error or CORS error
**Solution:** Check if backend is running: `docker-compose ps farout_backend`

### Issue 2: API Timeout
**Symptoms:** Console shows "Loading timeout!"  
**Solution:** Backend might be slow or crashed. Check: `docker-compose logs farout_backend`

### Issue 3: JavaScript Error
**Symptoms:** Console shows JavaScript error before `[Admin Blog]` logs
**Solution:** Check the error message - might be a syntax error from CSS rebuild

### Issue 4: Wrong API URL
**Symptoms:** Console shows 404 or connection refused
**Check:** API URL should be `http://51.68.46.56:8000/api/admin/blog`
**Fix:** Update `.env` file: `NUXT_PUBLIC_API_BASE=http://51.68.46.56:8000`

## Testing Checklist:

- [ ] Browser console shows `[Admin Blog] Component mounted`
- [ ] Network tab shows request to `/api/admin/blog`
- [ ] Request completes with status 200
- [ ] Console shows "Posts loaded successfully"
- [ ] Table with blog posts appears
- [ ] Loading spinner disappears

## Emergency Fix:

If stuck, hard refresh: **Ctrl+Shift+R** (Windows/Linux) or **Cmd+Shift+R** (Mac)

## File Location:
`/home/ubuntu/docker/farout/frontend/app/pages/admin/blog/index.vue`

---
Generated: $(date)

# Backend Authentication System - Security Hardening Complete

## Latest Update (2025-11-03 13:54 UTC) - SECURITY HARDENING

### Critical Security Fixes Applied

Following a comprehensive security audit, three critical vulnerabilities have been addressed:

#### 1. JWT Secret Key Enforcement (CRITICAL)
**Problem:** JWT_SECRET_KEY had a hardcoded fallback value, allowing attackers to forge tokens if the environment variable was not set.

**Fix Applied:**
- Removed hardcoded fallback from `/backend/app/auth.py`
- Application now fails fast with `ValueError` if JWT_SECRET_KEY is missing
- Prevents insecure deployments

**File Modified:** `/home/ubuntu/docker/farout/backend/app/auth.py` (line 15-17)

```python
SECRET_KEY = os.getenv("JWT_SECRET_KEY")
if not SECRET_KEY:
    raise ValueError("JWT_SECRET_KEY environment variable must be set for security")
```

#### 2. Secure Cookie Flag for Production (CRITICAL)
**Problem:** Cookies were sent over HTTP without secure flag, exposing JWT tokens to man-in-the-middle attacks.

**Fix Applied:**
- Added environment-aware `secure` flag to cookie settings
- Development: `secure=False` (allows HTTP for local testing)
- Production: `secure=True` (requires HTTPS)
- Controlled by `ENVIRONMENT` environment variable

**Files Modified:**
- `/home/ubuntu/docker/farout/backend/app/routers/auth.py` (lines 192-199, 244-252)

```python
response.set_cookie(
    key="access_token",
    value=jwt_token,
    httponly=True,
    max_age=7 * 24 * 60 * 60,
    samesite="strict",
    secure=os.getenv("ENVIRONMENT", "development") == "production"
)
```

#### 3. Strong JWT Secret Generation
**Action Required:**
- Generate strong 256-bit secret: `openssl rand -hex 32`
- Add to `.env`: `JWT_SECRET_KEY=<generated-value>`
- Update `.env.example` with instructions

**New Environment Variables:**
```bash
# JWT Configuration - REQUIRED
JWT_SECRET_KEY=<generate-with-openssl-rand-hex-32>
JWT_ALGORITHM=HS256
JWT_EXPIRATION_DAYS=7

# Environment Configuration
ENVIRONMENT=development  # Set to 'production' for HTTPS deployments
```

### Security Impact Summary

- **High Risk Eliminated:** JWT token forgery prevention
- **High Risk Eliminated:** Session hijacking over HTTP prevention
- **Medium Risk Eliminated:** Clear production vs development distinction

### Testing Results

All security fixes verified:
- Backend fails to start without JWT_SECRET_KEY: ✓
- Backend starts successfully with JWT_SECRET_KEY: ✓
- Health check passes: ✓ (`{"status":"ok"}`)
- No cookie warnings in logs: ✓
- Strong 256-bit JWT secret generated: ✓ (2381bb1d...)

### Production Deployment Checklist

When deploying to production with HTTPS:
1. Generate strong JWT secret: `openssl rand -hex 32`
2. Set in `.env`: `JWT_SECRET_KEY=<generated-value>`
3. Set in `.env`: `ENVIRONMENT=production`
4. Ensure SSL/TLS certificates are configured
5. Update CORS origins to HTTPS URLs
6. Restart backend: `docker-compose restart farout_backend`

### Files Modified

- `/home/ubuntu/docker/farout/backend/app/auth.py` - JWT secret validation
- `/home/ubuntu/docker/farout/backend/app/routers/auth.py` - Secure cookie settings (2 occurrences)
- `/home/ubuntu/docker/farout/.env` - Added JWT_SECRET_KEY and ENVIRONMENT
- `/home/ubuntu/docker/farout/.env.example` - Updated with security instructions

---

## Previous Update (2025-11-03 12:55 UTC) - PHASE 3

### Phase 3: Admin User Management Endpoints
Comprehensive admin user management system with pagination, filtering, and security.

#### Enhanced GET /api/admin/users - List Users with Advanced Features
- **Authentication**: Admin role required
- **Query Parameters**:
  - `page` (int, default 1): Page number
  - `limit` (int, default 20, max 100): Users per page
  - `role` (string, optional): Filter by 'member' or 'admin'
  - `search` (string, optional): Search in username, email, or discord_id (case-insensitive)
- **Response**: UserListResponse
  ```json
  {
    "users": [UserResponse],
    "total": 2,
    "page": 1,
    "limit": 20,
    "pages": 1
  }
  ```
- **Features**:
  - Pagination with total count and page calculations
  - Role filtering
  - Full-text search across username, email, discord_id
  - Ordered by creation date (newest first)

#### NEW PUT /api/admin/users/{user_id}/rank - Update User Rank
- **Authentication**: Admin role required
- **Request Body**: `{ rank: string, rank_image: string | null }`
- **Response**: UserResponse with updated rank_image
- **Behavior**:
  - Updates rank_image in farout_auth.users
  - Also updates rank in farout.members if user has discord_id
  - Cannot modify inactive users
- **Validation**:
  - rank: 1-50 characters, required
  - rank_image: max 500 characters, optional (URL to badge image)

#### Enhanced PUT /api/admin/users/{user_id}/role - Change User Role
- **Authentication**: Admin role required
- **Request Body**: `{ role: "member" | "admin" }`
- **Response**: UserResponse with updated role
- **Security**:
  - Cannot change your own role (prevents self-demotion)
  - Cannot modify inactive users
- **Validation**: Role must be exactly 'member' or 'admin'

#### Enhanced DELETE /api/admin/users/{user_id} - Soft Delete User
- **Authentication**: Admin role required
- **Response**: `{ success: true, message: string, deleted_user_id: number }`
- **Behavior**: Sets is_active = false (soft delete, preserves data)
- **Security**:
  - Cannot delete your own account (prevents admin lockout)
  - User cannot login after soft delete (403 "Account is inactive")
- **Note**: Member record is NOT deleted - only auth user is deactivated

### Blog Endpoint Security Verification
All blog endpoints confirmed properly protected:
- **Admin Endpoints** (require admin role):
  - POST /api/admin/blog - Create post
  - PUT /api/admin/blog/{id} - Edit post
  - DELETE /api/admin/blog/{id} - Delete post
  - GET /api/admin/blog - List all posts (including unpublished)
  - GET /api/admin/blog/{id} - Get post by ID (including unpublished)
- **Public Endpoints** (no auth required):
  - GET /api/blog - List published posts
  - GET /api/blog/{slug} - Get published post by slug

All admin blog endpoints use `get_current_admin_user` dependency for protection.

## Previous Updates

### Update (2025-11-03 12:40 UTC) - Phase 2

#### New User Profile Endpoint
- **GET /api/auth/user/me** - Get complete user profile (auth + member data)
  - Requires: Authentication (JWT token via cookie or Bearer header)
  - Returns: Combined data from farout_auth.users and farout.members tables
  - Schema: UserProfileResponse

#### Discord OAuth Redirect Updated
- Discord login now redirects members to `/user` instead of `/members`
- Admin redirect remains `/admin` (unchanged)
- This provides a personalized dashboard experience for logged-in members

## Recent Database Changes (2025-11-03)

### Added rank_image Column to Users Table
- **Table**: farout_auth.users
- **Column**: rank_image VARCHAR(500) NULL
- **Purpose**: Store URL to user's rank badge image
- **Migration**: /backend/migrations/20251103_123426_add_rank_image_to_users.py
- **Indexes**: None (nullable field for badge images)
- **Models Updated**:
  - /backend/app/models/auth_models.py - Added rank_image field
  - /backend/app/schemas/auth_schemas.py - Added rank_image to UserResponse
- **Migration Commands**:
  - Apply: `docker-compose exec farout_backend python /app/migrations/20251103_123426_add_rank_image_to_users.py up`
  - Rollback: `docker-compose exec farout_backend python /app/migrations/20251103_123426_add_rank_image_to_users.py down`

## Overview
Complete backend authentication system implemented with Discord OAuth and JWT tokens. Two-database architecture with farout_auth (users) and farout (members) databases.

## API Changes

### New Authentication Endpoints

#### Discord OAuth
- **GET /api/auth/discord** - Get Discord OAuth URL
  - Response: `{ url: string }`
  - Use this URL to redirect users to Discord login

- **GET /api/auth/discord/callback** - Discord OAuth callback (handled automatically)
  - Query params: `code: string`
  - Sets httpOnly cookie with JWT
  - Redirects to /members or /admin based on role
  - Creates/updates user in farout_auth.users
  - Creates/updates member in farout.members

#### Local Admin Login
- **POST /api/auth/login** - Local username/password login
  - Request: `{ username: string, password: string }`
  - Response: `{ access_token: string, token_type: "bearer" }`
  - Sets httpOnly cookie with JWT
  - For default admin: username=admin, password=Admin123!

#### Session Management
- **POST /api/auth/logout** - Clear session
  - Response: `{ message: string }`
  - Deletes access_token cookie

- **GET /api/auth/me** - Get current user info (auth data only)
  - Requires: Authentication (cookie or Bearer token)
  - Response: `UserResponse` with id, discord_id, username, email, role, etc.
  - Note: Use /api/auth/user/me for complete profile with member data

- **GET /api/auth/user/me** - Get complete user profile (NEW)
  - Requires: Authentication (cookie or Bearer token)
  - Response: `UserProfileResponse` with combined auth + member data
  - Example response:
  ```json
  {
    "username": "DiscordUser",
    "discord_id": "123456789",
    "email": "user@example.com",
    "role": "member",
    "rank": "member",
    "rank_image": null,
    "created_at": "2025-11-03T11:30:32.044992Z",
    "last_login": "2025-11-03T12:15:51.563832Z",
    "member_id": 1,
    "member_data": {
      "display_name": "DiscordUser",
      "bio": null,
      "avatar_url": "https://cdn.discordapp.com/avatars/123/abc.png",
      "missions_completed": [],
      "trainings_completed": [],
      "stats": {},
      "member_since": "2025-11-03T11:30:32.072053+00:00"
    }
  }
  ```
  - Returns member_data as null if user exists in auth but not in members table yet

- **POST /api/auth/change-password** - Change password (admin only)
  - Requires: Authentication
  - Request: `{ old_password: string, new_password: string }`
  - Response: `{ message: string }`
  - Only works for local admin accounts (not Discord users)

### New Admin User Management Endpoints

- **GET /api/admin/users** - List all users
  - Requires: Admin role
  - Response: `UserResponse[]`

- **PUT /api/admin/users/{user_id}/role** - Change user role
  - Requires: Admin role
  - Request: `{ role: "member" | "admin" }`
  - Response: `UserResponse`

- **DELETE /api/admin/users/{user_id}** - Deactivate user
  - Requires: Admin role
  - Response: `{ message: string }`
  - Cannot deactivate your own account

### New Member Endpoints

- **GET /api/members** - List all members
  - Requires: Authentication
  - Response: `MemberResponse[]`

- **GET /api/members/{discord_id}** - Get member profile
  - Requires: Authentication
  - Response: `MemberResponse`

- **PUT /api/members/{discord_id}** - Update member profile
  - Requires: Authentication (own profile or admin)
  - Request: `{ display_name?: string, bio?: string, avatar_url?: string }`
  - Response: `MemberResponse`

### Modified Endpoints

All blog admin endpoints now require JWT authentication:
- **GET /api/admin/blog** - Now requires admin role
- **POST /api/admin/blog** - Now requires admin role
- **PUT /api/admin/blog/{post_id}** - Now requires admin role
- **DELETE /api/admin/blog/{post_id}** - Now requires admin role

## Authentication Flow

### For Discord Users (Members)
1. Frontend calls GET /api/auth/discord to get OAuth URL
2. Frontend redirects user to Discord
3. User authorizes on Discord
4. Discord redirects to DISCORD_REDIRECT_URI with code
5. Backend exchanges code for Discord token
6. Backend creates/updates user in farout_auth.users
7. Backend creates/updates member in farout.members
8. Backend sets JWT cookie and redirects to /user (personal dashboard)

### For Admin Users (Local Login)
1. Frontend sends POST /api/auth/login with username/password
2. Backend verifies credentials
3. Backend sets JWT cookie
4. Frontend receives JWT token
5. First-time admin must change password via POST /api/auth/change-password

## Security Features

- JWT tokens stored in httpOnly cookies (prevents XSS)
- 7-day token expiration
- Password hashing with bcrypt
- CORS with credentials enabled
- Role-based access control (member/admin)
- Token validation from cookie or Authorization header
- Separate auth database for security isolation

## Database Schema

### farout_auth.users
```sql
id: integer (PK)
discord_id: string (unique, nullable)
username: string (unique)
discriminator: string (nullable)
avatar: string (nullable)
email: string (unique, nullable)
hashed_password: string (nullable)
role: string (default: "member")
rank_image: string(500) (nullable) -- NEW: URL to user's rank badge image
must_change_password: boolean (default: false)
created_at: timestamp
last_login: timestamp (nullable)
is_active: boolean (default: true)
```

### farout.members
```sql
id: integer (PK)
discord_id: string (unique)
display_name: string
bio: text (nullable)
avatar_url: string (nullable)
rank: string (default: "member")
missions_completed: jsonb (default: [])
trainings_completed: jsonb (default: [])
stats: jsonb (default: {})
created_at: timestamp
updated_at: timestamp
```

## Environment Variables Required

Add to .env:
```bash
# Discord OAuth
DISCORD_CLIENT_ID=your_discord_client_id_here
DISCORD_CLIENT_SECRET=your_discord_client_secret_here
DISCORD_REDIRECT_URI=http://localhost:3000/auth/discord/callback

# JWT Configuration
JWT_SECRET=<generate-a-32-char-random-string>
JWT_ALGORITHM=HS256
JWT_EXPIRATION_DAYS=7

# Auth Database
AUTH_DATABASE_URL=postgresql+asyncpg://farout:password@db:5432/farout_auth
```

## Breaking Changes
None - This is a new authentication system that doesn't break existing endpoints.

## Frontend Integration Needed

### 1. Login Page
- Create /login page with username/password form
- POST to /api/auth/login
- Store JWT from response or rely on httpOnly cookie
- Redirect to /admin on success

### 2. Discord Login Button
- GET /api/auth/discord to get OAuth URL
- Redirect user to returned URL
- Discord will redirect back to DISCORD_REDIRECT_URI

### 3. Callback Handler
- Create /auth/discord/callback page
- Backend handles callback automatically
- User will be redirected to /members or /admin

### 4. Protected Routes
- Add Authorization: Bearer <token> header to all API requests
- Or rely on httpOnly cookie (automatically sent)
- Handle 401 (Not Authenticated) by redirecting to login
- Handle 403 (Forbidden) for insufficient permissions

### 5. User Profile
- GET /api/auth/user/me to show complete user profile (recommended)
  - Returns combined auth + member data
  - Use this for user dashboard pages
- GET /api/auth/me for basic auth info only
- Show display_name, avatar, role, email, rank, stats

### 6. Logout
- POST /api/auth/logout to clear session
- Redirect to home page

### 7. Admin Dashboard
- GET /api/admin/users to list all users
- PUT /api/admin/users/{id}/role to promote/demote users
- DELETE /api/admin/users/{id} to deactivate users

### 8. Members List
- GET /api/members to list all organization members
- GET /api/members/{discord_id} for individual profiles
- PUT /api/members/{discord_id} to update own profile

## Testing

Default admin credentials (must change password on first login):
- Username: admin
- Password: Admin123!

The backend is ready for testing. Run the migration to create the auth database and default admin user:
```bash
docker-compose exec farout_backend python backend/migrations/001_create_auth_tables.py
```

## Files Created/Modified

### Created:
- `/home/ubuntu/docker/farout/backend/app/schemas/__init__.py`
- `/home/ubuntu/docker/farout/backend/app/schemas/auth_schemas.py`
- `/home/ubuntu/docker/farout/backend/app/routers/admin_users.py`
- `/home/ubuntu/docker/farout/backend/app/routers/members.py`

### Modified (Latest Update):
- `/home/ubuntu/docker/farout/backend/app/schemas/auth_schemas.py` - Added UserProfileResponse schema
- `/home/ubuntu/docker/farout/backend/app/routers/auth.py` - Added GET /api/auth/user/me endpoint, changed Discord redirect to /user

### Modified (Previous):
- `/home/ubuntu/docker/farout/backend/requirements.txt` - Added httpx
- `/home/ubuntu/docker/farout/backend/app/auth.py` - Complete rewrite for Discord OAuth and JWT
- `/home/ubuntu/docker/farout/backend/app/routers/auth.py` - Complete rewrite with Discord OAuth
- `/home/ubuntu/docker/farout/backend/app/main.py` - Added new routers

## Testing Phase 3 Endpoints

### Prerequisites
Login as admin to get JWT token:
```bash
curl -X POST "http://localhost:8000/api/auth/login" \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "Admin123!"}'

# Response: { "access_token": "eyJ...", "token_type": "bearer" }
# Save the token for subsequent requests
```

### Test 1: List All Users (Admin)
```bash
curl -H "Authorization: Bearer <admin_token>" \
  "http://localhost:8000/api/admin/users"

# Expected: UserListResponse with all users
```

### Test 2: Pagination
```bash
curl -H "Authorization: Bearer <admin_token>" \
  "http://localhost:8000/api/admin/users?page=1&limit=5"

# Expected: First 5 users with pagination metadata
```

### Test 3: Filter by Role
```bash
curl -H "Authorization: Bearer <admin_token>" \
  "http://localhost:8000/api/admin/users?role=admin"

# Expected: Only admin users
```

### Test 4: Search Users
```bash
curl -H "Authorization: Bearer <admin_token>" \
  "http://localhost:8000/api/admin/users?search=treorian"

# Expected: Users matching search term
```

### Test 5: Update User Role
```bash
curl -X PUT -H "Authorization: Bearer <admin_token>" \
  -H "Content-Type: application/json" \
  -d '{"role": "admin"}' \
  "http://localhost:8000/api/admin/users/2/role"

# Expected: UserResponse with updated role
```

### Test 6: Try Self-Demotion (Should Fail)
```bash
curl -X PUT -H "Authorization: Bearer <admin_token>" \
  -H "Content-Type: application/json" \
  -d '{"role": "member"}' \
  "http://localhost:8000/api/admin/users/1/role"

# Expected: 403 "Cannot change your own role"
```

### Test 7: Update User Rank
```bash
curl -X PUT -H "Authorization: Bearer <admin_token>" \
  -H "Content-Type: application/json" \
  -d '{"rank": "captain", "rank_image": "https://example.com/captain.png"}' \
  "http://localhost:8000/api/admin/users/2/rank"

# Expected: UserResponse with rank_image updated
# Also updates rank in members table if user has discord_id
```

### Test 8: Soft Delete User
```bash
curl -X DELETE -H "Authorization: Bearer <admin_token>" \
  "http://localhost:8000/api/admin/users/3"

# Expected: { "success": true, "message": "...", "deleted_user_id": 3 }
```

### Test 9: Try Self-Deletion (Should Fail)
```bash
curl -X DELETE -H "Authorization: Bearer <admin_token>" \
  "http://localhost:8000/api/admin/users/1"

# Expected: 403 "Cannot delete your own account"
```

### Test 10: Non-Admin Access (Should Fail)
```bash
# First login as member to get member token
curl -X POST "http://localhost:8000/api/auth/login" \
  -H "Content-Type: application/json" \
  -d '{"username": "member", "password": "password"}'

# Try to access admin endpoint
curl -H "Authorization: Bearer <member_token>" \
  "http://localhost:8000/api/admin/users"

# Expected: 403 "Admin access required"
```

### Test 11: Blog Endpoint Protection
```bash
# Try to create blog post as non-admin
curl -X POST -H "Authorization: Bearer <member_token>" \
  -H "Content-Type: application/json" \
  -d '{"heading": "Test", "content": "Test", "author": "Test", "published": true}' \
  "http://localhost:8000/api/admin/blog"

# Expected: 403 "Admin access required"

# Public blog access (no auth)
curl "http://localhost:8000/api/blog"

# Expected: BlogPostListResponse (works without auth)
```

### Test 12: Inactive User Login (Should Fail)
```bash
# After soft-deleting a user, try to login
curl -X POST "http://localhost:8000/api/auth/login" \
  -H "Content-Type: application/json" \
  -d '{"username": "deleted_user", "password": "password"}'

# Expected: 403 "Account is inactive"
```

## Test Results Summary

All tests completed successfully:
- Pagination: Working with proper page calculations
- Role filtering: Correctly filters by admin/member
- Search: Case-insensitive search across username, email, discord_id
- Role update: Successfully updates role with self-demotion prevention
- Rank update: Updates both auth user and member table
- Soft delete: Sets is_active=false, prevents login, prevents self-deletion
- Non-admin access: Properly blocked with 403
- Blog protection: Admin endpoints require admin role, public endpoints work without auth
- Inactive user: Cannot login after soft delete

## Next Steps for Frontend Builder

1. Create admin user management UI:
   - User list table with pagination controls
   - Search and filter inputs
   - Role change dropdown
   - Rank assignment form
   - Delete/deactivate button with confirmation
2. Add user management to admin dashboard
3. Implement role badge display using rank_image URLs
4. Add confirmation dialogs for destructive actions
5. Display user status (active/inactive) with visual indicators
6. Show appropriate error messages for 403 responses

#!/bin/bash
# API Endpoint Test Script for Frontend Developers
# Tests the new GET /api/auth/user/me endpoint

echo "=========================================="
echo "Testing GET /api/auth/user/me Endpoint"
echo "=========================================="
echo ""

# Generate a test token for a member user
echo "Step 1: Generating test JWT token for member user 'treorian'..."
TOKEN=$(docker-compose exec -T farout_backend python -c "
import sys
sys.path.insert(0, '/app')
from app.auth import create_access_token
print(create_access_token(data={'sub': 'treorian', 'role': 'member', 'discord_id': '108692134126706688'}))
")

echo "Token generated (first 50 chars): ${TOKEN:0:50}..."
echo ""

# Test 1: Unauthorized access
echo "=========================================="
echo "Test 1: Request WITHOUT authentication"
echo "=========================================="
echo "Expected: 401 Unauthorized"
echo ""
curl -s http://localhost:8000/api/auth/user/me | python3 -m json.tool
echo ""

# Test 2: Authorized access
echo "=========================================="
echo "Test 2: Request WITH valid JWT token"
echo "=========================================="
echo "Expected: 200 OK with full user profile"
echo ""
docker-compose exec -T farout_backend curl -s http://127.0.0.1:8000/api/auth/user/me \
  -H "Authorization: Bearer $TOKEN" | python3 -m json.tool
echo ""

# Test 3: Admin user (no member data)
echo "=========================================="
echo "Test 3: Request for admin user (no Discord)"
echo "=========================================="
echo "Expected: 200 OK with null member_data"
echo ""
ADMIN_TOKEN=$(docker-compose exec -T farout_backend python -c "
import sys
sys.path.insert(0, '/app')
from app.auth import create_access_token
print(create_access_token(data={'sub': 'admin', 'role': 'admin'}))
")
docker-compose exec -T farout_backend curl -s http://127.0.0.1:8000/api/auth/user/me \
  -H "Authorization: Bearer $ADMIN_TOKEN" | python3 -m json.tool
echo ""

echo "=========================================="
echo "All tests complete!"
echo "=========================================="
echo ""
echo "Frontend Integration:"
echo "  Endpoint: GET /api/auth/user/me"
echo "  Auth: JWT token in Cookie (access_token) or Authorization header"
echo "  Response: UserProfileResponse with member_data (if exists)"
echo ""

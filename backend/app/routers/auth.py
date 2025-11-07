"""
Authentication router with Discord OAuth and local admin login
"""
from fastapi import APIRouter, Depends, HTTPException, status, Response, Request
from fastapi.responses import RedirectResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
import httpx
import os
import secrets
from datetime import datetime

from ..database.auth_db import get_auth_db
from ..db import SessionLocal as AppSessionLocal
from ..models.auth_models import User
from ..models.member_models import Member
from ..schemas.auth_schemas import (
    UserLogin, UserResponse, Token, PasswordChange, UserProfileResponse
)
from ..auth import (
    verify_password, get_password_hash, create_access_token,
    get_current_user
)

router = APIRouter(prefix="/auth", tags=["authentication"])

# Discord OAuth configuration
DISCORD_CLIENT_ID = os.getenv("DISCORD_CLIENT_ID")
DISCORD_CLIENT_SECRET = os.getenv("DISCORD_CLIENT_SECRET")
DISCORD_REDIRECT_URI = os.getenv("DISCORD_REDIRECT_URI")
DISCORD_API_BASE = "https://discord.com/api/v10"

@router.get("/discord")
async def discord_login(response: Response):
    """Redirect to Discord OAuth with CSRF protection"""
    # Generate state parameter for CSRF protection
    state = secrets.token_urlsafe(32)

    discord_oauth_url = (
        f"https://discord.com/api/oauth2/authorize"
        f"?client_id={DISCORD_CLIENT_ID}"
        f"&redirect_uri={DISCORD_REDIRECT_URI}"
        f"&response_type=code"
        f"&scope=identify%20email"
        f"&state={state}"
    )

    # Store state in httpOnly cookie for validation in callback
    response.set_cookie(
        key="oauth_state",
        value=state,
        httponly=True,
        max_age=300,  # 5 minutes
        samesite="lax"
    )

    return {"url": discord_oauth_url}

@router.get("/discord/callback")
async def discord_callback(
    request: Request,
    auth_db: AsyncSession = Depends(get_auth_db),
    code: str = None,
    state: str = None,
    error: str = None,
    error_description: str = None
):
    """Handle Discord OAuth callback with CSRF protection"""

    # Check for OAuth errors (user denied, etc.)
    if error:
        raise HTTPException(
            status_code=400,
            detail=f"Discord OAuth error: {error} - {error_description or 'No description'}"
        )

    # Validate required parameters
    if not code or not state:
        raise HTTPException(
            status_code=400,
            detail="Missing required OAuth parameters"
        )

    # Validate state parameter (CSRF protection)
    stored_state = request.cookies.get("oauth_state")
    if not stored_state or stored_state != state:
        raise HTTPException(
            status_code=400,
            detail="Invalid OAuth state parameter - possible CSRF attack"
        )

    # Exchange code for access token
    async with httpx.AsyncClient() as client:
        token_response = await client.post(
            f"{DISCORD_API_BASE}/oauth2/token",
            data={
                "client_id": DISCORD_CLIENT_ID,
                "client_secret": DISCORD_CLIENT_SECRET,
                "grant_type": "authorization_code",
                "code": code,
                "redirect_uri": DISCORD_REDIRECT_URI
            },
            headers={"Content-Type": "application/x-www-form-urlencoded"}
        )

        if token_response.status_code != 200:
            raise HTTPException(status_code=400, detail="Failed to get Discord token")

        token_data = token_response.json()
        access_token = token_data["access_token"]

        # Get user info from Discord
        user_response = await client.get(
            f"{DISCORD_API_BASE}/users/@me",
            headers={"Authorization": f"Bearer {access_token}"}
        )

        if user_response.status_code != 200:
            raise HTTPException(status_code=400, detail="Failed to get Discord user info")

        discord_user = user_response.json()

    # Create or update user in farout_auth.users
    discord_id = discord_user["id"]
    username = discord_user["username"]
    discriminator = discord_user.get("discriminator")
    avatar = discord_user.get("avatar")
    email = discord_user.get("email")

    result = await auth_db.execute(select(User).where(User.discord_id == discord_id))
    user = result.scalar_one_or_none()

    if user:
        # Update existing user
        user.username = username
        user.discriminator = discriminator
        user.avatar = avatar
        user.email = email
        user.last_login = datetime.utcnow()
    else:
        # Create new user
        user = User(
            discord_id=discord_id,
            username=username,
            discriminator=discriminator,
            avatar=avatar,
            email=email,
            role="member",
            last_login=datetime.utcnow()
        )
        auth_db.add(user)

    await auth_db.commit()
    await auth_db.refresh(user)

    # Create or update member profile in farout.members
    async with AppSessionLocal() as app_db:
        result = await app_db.execute(select(Member).where(Member.discord_id == discord_id))
        member = result.scalar_one_or_none()

        avatar_url = f"https://cdn.discordapp.com/avatars/{discord_id}/{avatar}.png" if avatar else None

        if member:
            # Update existing member
            member.display_name = username
            member.avatar_url = avatar_url
        else:
            # Create new member
            member = Member(
                discord_id=discord_id,
                display_name=username,
                avatar_url=avatar_url
            )
            app_db.add(member)

        await app_db.commit()

    # Create JWT token
    jwt_token = create_access_token(
        data={"sub": user.username, "role": user.role, "discord_id": discord_id}
    )

    # Determine frontend redirect URL
    frontend_base = os.getenv("FRONTEND_URL")
    if not frontend_base:
        raise ValueError("FRONTEND_URL environment variable must be set for OAuth redirects")
    redirect_path = "/user" if user.role == "member" else "/admin"
    redirect_url = f"{frontend_base}{redirect_path}"

    # Create redirect response
    response = RedirectResponse(url=redirect_url)

    # Set authentication cookie with secure settings
    response.set_cookie(
        key="access_token",
        value=jwt_token,
        httponly=True,
        max_age=7 * 24 * 60 * 60,  # 7 days
        samesite="strict",
        secure=os.getenv("ENVIRONMENT", "development") == "production"  # Enable in production
    )

    # Clear the oauth_state cookie after successful authentication
    response.delete_cookie(key="oauth_state")

    return response

@router.post("/login", response_model=Token)
async def login(
    user_login: UserLogin,
    response: Response,
    db: AsyncSession = Depends(get_auth_db)
):
    """Local admin login"""

    result = await db.execute(select(User).where(User.username == user_login.username))
    user = result.scalar_one_or_none()

    if not user or not user.hashed_password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password"
        )

    if not verify_password(user_login.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password"
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Account is inactive"
        )

    # Update last login
    user.last_login = datetime.utcnow()
    await db.commit()

    # Create JWT token
    access_token = create_access_token(
        data={"sub": user.username, "role": user.role}
    )

    # Set httpOnly cookie with secure settings
    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        max_age=7 * 24 * 60 * 60,  # 7 days
        samesite="strict",
        secure=os.getenv("ENVIRONMENT", "development") == "production"  # Enable in production
    )

    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/logout")
async def logout(response: Response):
    """Logout and clear session"""
    response.delete_cookie(key="access_token")
    return {"message": "Logged out successfully"}

@router.get("/me", response_model=UserResponse)
async def get_current_user_info(current_user: User = Depends(get_current_user)):
    """Get current user info"""
    return current_user

@router.get("/user/me", response_model=UserProfileResponse)
async def get_user_profile(current_user: User = Depends(get_current_user)):
    """Get current user's complete profile (auth + member data)"""

    # Start with auth data
    profile_data = {
        "username": current_user.username,
        "discord_id": current_user.discord_id,
        "email": current_user.email,
        "role": current_user.role,
        "rank": "member",  # Default rank
        "rank_image": current_user.rank_image,
        "created_at": current_user.created_at,
        "last_login": current_user.last_login,
        "member_id": None,
        "member_data": None
    }

    # Try to get member data from farout.members if user has discord_id
    if current_user.discord_id:
        async with AppSessionLocal() as app_db:
            result = await app_db.execute(
                select(Member).where(Member.discord_id == current_user.discord_id)
            )
            member = result.scalar_one_or_none()

            if member:
                profile_data["member_id"] = member.id
                profile_data["rank"] = member.rank
                profile_data["member_data"] = {
                    "display_name": member.display_name,
                    "bio": member.bio,
                    "avatar_url": member.avatar_url,
                    "missions_completed": member.missions_completed,
                    "trainings_completed": member.trainings_completed,
                    "stats": member.stats,
                    "member_since": member.created_at.isoformat() if member.created_at else None
                }

    return UserProfileResponse(**profile_data)

@router.post("/change-password")
async def change_password(
    password_change: PasswordChange,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_auth_db)
):
    """Change password (for admin first login)"""

    if not current_user.hashed_password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Password change not available for Discord users"
        )

    if not verify_password(password_change.old_password, current_user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect old password"
        )

    # Update password
    current_user.hashed_password = get_password_hash(password_change.new_password)
    current_user.must_change_password = False
    await db.commit()

    return {"message": "Password changed successfully"}

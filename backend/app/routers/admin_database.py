"""
Admin routes for database connection management
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy import text
from pydantic import BaseModel
from typing import Optional, Dict, Any
import os

from ..auth import require_admin
from ..models.auth_models import User
from ..database.auth_db import get_auth_db

router = APIRouter(prefix="/admin/database", tags=["admin-database"])

class DatabaseConnectionTest(BaseModel):
    host: str
    port: int
    database: str
    username: str
    password: str

class DatabaseStatus(BaseModel):
    database_name: str
    connected: bool
    host: str
    port: str
    tables_count: Optional[int] = None
    error: Optional[str] = None

@router.get("/status", dependencies=[Depends(require_admin)])
async def get_database_status(
    current_user: User = Depends(require_admin)
) -> Dict[str, DatabaseStatus]:
    """Get status of all configured databases"""
    
    statuses = {}
    
    # Check farout database
    try:
        from ..db import engine as app_engine
        async with app_engine.connect() as conn:
            result = await conn.execute(text("""
                SELECT COUNT(*) 
                FROM information_schema.tables 
                WHERE table_schema = 'public'
            """))
            table_count = result.scalar()
            
            statuses["farout"] = DatabaseStatus(
                database_name="farout",
                connected=True,
                host=os.getenv("DATABASE_HOST", "db"),
                port=os.getenv("DATABASE_PORT", "5432"),
                tables_count=table_count
            )
    except Exception as e:
        statuses["farout"] = DatabaseStatus(
            database_name="farout",
            connected=False,
            host=os.getenv("DATABASE_HOST", "db"),
            port=os.getenv("DATABASE_PORT", "5432"),
            error=str(e)
        )
    
    # Check farout_auth database
    try:
        from ..database.auth_db import auth_engine
        async with auth_engine.connect() as conn:
            result = await conn.execute(text("""
                SELECT COUNT(*) 
                FROM information_schema.tables 
                WHERE table_schema = 'public'
            """))
            table_count = result.scalar()
            
            auth_url = os.getenv("AUTH_DATABASE_URL", "")
            # Parse connection string for display (hide password)
            import re
            match = re.search(r'@([^:]+):(\d+)', auth_url)
            host = match.group(1) if match else "unknown"
            port = match.group(2) if match else "unknown"
            
            statuses["farout_auth"] = DatabaseStatus(
                database_name="farout_auth",
                connected=True,
                host=host,
                port=port,
                tables_count=table_count
            )
    except Exception as e:
        statuses["farout_auth"] = DatabaseStatus(
            database_name="farout_auth",
            connected=False,
            host="unknown",
            port="unknown",
            error=str(e)
        )
    
    return statuses

@router.post("/test-connection", dependencies=[Depends(require_admin)])
async def test_database_connection(
    connection: DatabaseConnectionTest,
    current_user: User = Depends(require_admin)
) -> Dict[str, Any]:
    """Test a database connection without saving it"""
    
    connection_string = (
        f"postgresql+asyncpg://{connection.username}:{connection.password}"
        f"@{connection.host}:{connection.port}/{connection.database}"
    )
    
    try:
        test_engine = create_async_engine(connection_string, echo=False)
        async with test_engine.connect() as conn:
            await conn.execute(text("SELECT 1"))
        
        await test_engine.dispose()
        
        return {
            "success": True,
            "message": f"Successfully connected to {connection.database}",
            "database": connection.database,
            "host": connection.host,
            "port": connection.port
        }
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"Connection failed: {str(e)}"
        )

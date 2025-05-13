from fastapi import APIRouter, HTTPException, Query

from database.database import Database
from config import Config

from ..models.models import UserModel


router = APIRouter(
    prefix="/users",
    tags=["users"],
    responses={404: {"description": "Not found"}}
)
cfg = Config()
db = Database(
    host=cfg.DB_INFO['host'],
    user=cfg.DB_INFO['user'],
    password=cfg.DB_INFO['password'],
    database=cfg.DB_INFO['database']
)

@router.get("/")
async def root_users():
    """Check connection to users."""
    return ({"message": "Hello from users!"})


@router.post("/add")
async def create_user(user: UserModel):
    """Create a new user in the database using a Telegram ID as a query parameter."""

    try:
        result = await db.register_user(telegram_id=user.telegram_id)
        if result:
            return (
                {"data": {
                    "telegram_id": user.telegram_id,
                    "status": "created"
                },
                "meta": {}}
            )
        else:
            raise HTTPException(409, detail="User already exists")
        
    except ValueError as e:
        raise HTTPException(409, detail=str(e))
    
    except RuntimeError as e:
        raise HTTPException(500, detail="Internal server error")
    
@router.get("/get")
async def get(telegram_id: str = Query(..., description="Telegram ID of the user")):
    """Get a user from the database using a Telegram ID as a query parameter."""

    try:
        result = await db.get_user(telegram_id=telegram_id)
        if result:
            return (
                {"data": {
                    "user_id": result,
                    "status": "found"
                },
                "meta": {}}
            )
        else:
            raise HTTPException(404, detail="User not found")
        
    except ValueError as e:
        raise HTTPException(404, detail=str(e))
    
    except RuntimeError as e:
        raise HTTPException(500, detail="Internal server error")
    

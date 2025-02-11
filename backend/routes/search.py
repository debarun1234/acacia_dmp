from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import User, Desk

search_router = APIRouter()

@search_router.get("/search/{user_name}")
def search_user(user_name: str, db: Session = Depends(get_db)):
    """ Search for a user’s desk across all floors """
    user_name = user_name.strip().lower()
    result = None

    # Iterate through all desks to find a match
    desks = db.query(Desk).filter(Desk.status == "occupied").all()
    for desk in desks:
        user = db.query(User).filter(User.id == desk.user_id).first()
        if user and user.username.lower().startswith(user_name):  # Partial match
            result = {
                "desk_id": desk.desk_id,
                "floor": desk.floor,
                "tech_area": desk.tech_area,
                "user": user.username
            }
            break  # Stop on first match

    if result:
        return result
    else:
        raise HTTPException(status_code=404, detail="User not found on any floor")

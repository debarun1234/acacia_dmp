from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import Desk, User
from schemas import DeskUpdate
import jwt
import os

SECRET_KEY = os.getenv("SECRET_KEY", "myjwtsecret")

desk_router = APIRouter()

def verify_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")

@desk_router.get("/desks/{floor}")
def get_desks(floor: str, db: Session = Depends(get_db)):
    """ Get all desks for a specific floor """
    desks = db.query(Desk).filter(Desk.floor == floor).all()
    return desks

@desk_router.post("/desk/update/{floor}/{desk_id}")
def update_desk(floor: str, desk_id: str, desk_update: DeskUpdate, token: str, db: Session = Depends(get_db)):
    """ Update desk status only if user is authorized """
    user_data = verify_token(token)
    user = db.query(User).filter(User.id == user_data["user_id"]).first()
    
    desk = db.query(Desk).filter(Desk.desk_id == desk_id, Desk.floor == floor).first()
    if not desk:
        raise HTTPException(status_code=404, detail="Desk not found")

    if desk.tech_area != user.tech_area:
        raise HTTPException(status_code=403, detail="You can only book desks in your tech area")

    desk.status = desk_update.status
    desk.user_id = user.id if desk_update.status == "occupied" else None
    db.commit()

    return {"message": "Desk updated successfully"}

@desk_router.get("/search/{username}")
def search_user(username: str, db: Session = Depends(get_db)):
    """ Search for a user and return their desk & floor """
    user = db.query(User).filter(User.username.ilike(f"%{username}%")).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    desk = db.query(Desk).filter(Desk.user_id == user.id).first()
    if not desk:
        raise HTTPException(status_code=404, detail="User is not currently occupying any desk")

    return {"desk_id": desk.desk_id, "floor": desk.floor}
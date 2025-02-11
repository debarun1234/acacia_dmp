from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import User
from schemas import UserLogin
from auth import verify_token
from werkzeug.security import generate_password_hash

user_router = APIRouter()

@user_router.get("/profile")
def get_profile(token: str, db: Session = Depends(get_db)):
    """ Get user profile """
    user_data = verify_token(token)
    user = db.query(User).filter(User.id == user_data["user_id"]).first()
    return {"username": user.username, "tech_area": user.tech_area, "role": user.role}

@user_router.put("/update-password")
def update_password(user_login: UserLogin, token: str, db: Session = Depends(get_db)):
    """ Update user password """
    user_data = verify_token(token)
    user = db.query(User).filter(User.id == user_data["user_id"]).first()
    
    if not user.verify_password(user_login.password):
        raise HTTPException(status_code=401, detail="Incorrect password")
    
    user.password_hash = generate_password_hash(user_login.password)
    db.commit()
    
    return {"message": "Password updated successfully"}

@user_router.delete("/delete")
def delete_account(token: str, db: Session = Depends(get_db)):
    """ Delete user account """
    user_data = verify_token(token)
    user = db.query(User).filter(User.id == user_data["user_id"]).first()
    
    db.delete(user)
    db.commit()
    
    return {"message": "User account deleted successfully"}

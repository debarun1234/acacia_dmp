from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from database import get_db
from models import User, Desk
import jwt
import os
import json
from werkzeug.security import generate_password_hash

SECRET_KEY = os.getenv("SECRET_KEY", "myjwtsecret")

admin_router = APIRouter()

def verify_admin(token: str, db: Session):
    """ Verify if the token belongs to an admin user """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        user_id = payload["user_id"]
        user = db.query(User).filter(User.id == user_id).first()
        if not user or user.role != "admin":
            raise HTTPException(status_code=403, detail="Admin access required")
        return user
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")

# -------------------- 🟢 LOAD JSON DATA --------------------

@admin_router.post("/load-users/")
def load_users(file: UploadFile = File(...), token: str = None, db: Session = Depends(get_db)):
    """ Load users from a JSON file (Admin only) """
    verify_admin(token, db)
    try:
        contents = file.file.read()
        users_data = json.loads(contents)
        
        for user in users_data["users"]:
            existing_user = db.query(User).filter(User.username == user["username"]).first()
            if not existing_user:
                new_user = User(
                    username=user["username"],
                    password_hash=generate_password_hash(user["password"]),
                    tech_area=user["tech_area"],
                    role=user["role"]
                )
                db.add(new_user)
        db.commit()
        return {"message": "Users imported successfully"}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error importing users: {str(e)}")

@admin_router.post("/load-desks/")
def load_desks(file: UploadFile = File(...), token: str = None, db: Session = Depends(get_db)):
    """ Load desks from a JSON file (Admin only) """
    verify_admin(token, db)
    try:
        contents = file.file.read()
        desks_data = json.loads(contents)
        
        for desk_id, details in desks_data["desks"].items():
            existing_desk = db.query(Desk).filter(Desk.desk_id == desk_id).first()
            if not existing_desk:
                new_desk = Desk(
                    desk_id=desk_id,
                    floor=details["floor"],
                    status=details["status"],
                    tech_area=details["tech_area"]
                )
                db.add(new_desk)
        db.commit()
        return {"message": "Desks imported successfully"}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error importing desks: {str(e)}")


# -------------------- 🔵 VIEW USERS & DESKS --------------------

@admin_router.get("/users/")
def list_users(token: str, db: Session = Depends(get_db)):
    """ Get all users (Admin only) """
    verify_admin(token, db)
    return db.query(User).all()

@admin_router.get("/users/{tech_area}")
def list_users_by_tech_area(tech_area: str, token: str, db: Session = Depends(get_db)):
    """ Get users by tech area (Admin only) """
    verify_admin(token, db)
    return db.query(User).filter(User.tech_area == tech_area).all()

@admin_router.get("/desks/")
def list_desks(token: str, db: Session = Depends(get_db)):
    """ Get all desks (Admin only) """
    verify_admin(token, db)
    return db.query(Desk).all()

@admin_router.get("/desks/{tech_area}")
def list_desks_by_tech_area(tech_area: str, token: str, db: Session = Depends(get_db)):
    """ Get desks by tech area (Admin only) """
    verify_admin(token, db)
    return db.query(Desk).filter(Desk.tech_area == tech_area).all()


# -------------------- 🔴 USER MANAGEMENT --------------------

@admin_router.delete("/user/{user_id}")
def delete_user(user_id: int, token: str, db: Session = Depends(get_db)):
    """ Delete a user (Admin only) """
    verify_admin(token, db)
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    db.delete(user)
    db.commit()
    return {"message": "User deleted successfully"}

@admin_router.put("/user/update-password/{user_id}")
def update_user_password(user_id: int, new_password: str, token: str, db: Session = Depends(get_db)):
    """ Update a user's password (Admin only) """
    verify_admin(token, db)
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    user.password_hash = generate_password_hash(new_password)
    db.commit()
    return {"message": "User password updated successfully"}

@admin_router.put("/user/update-tech-area/{user_id}")
def update_user_tech_area(user_id: int, new_tech_area: str, token: str, db: Session = Depends(get_db)):
    """ Update a user's tech area (Admin only) """
    verify_admin(token, db)
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    user.tech_area = new_tech_area
    db.commit()
    return {"message": "User tech area updated successfully"}


# -------------------- 🟠 RESET FLOOR DESKS --------------------

@admin_router.post("/reset-floor/{floor}")
def reset_floor(floor: str, token: str, db: Session = Depends(get_db)):
    """ Reset all desks on a floor (Admin only) """
    verify_admin(token, db)
    desks = db.query(Desk).filter(Desk.floor == floor).all()
    for desk in desks:
        desk.status = "available"
        desk.user_id = None
    db.commit()
    return {"message": f"All desks on {floor} have been reset"}

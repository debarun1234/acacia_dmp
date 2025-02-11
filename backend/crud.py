from sqlalchemy.orm import Session
from models import User, Desk
from werkzeug.security import generate_password_hash

def get_user_by_username(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()

def create_user(db: Session, username: str, password: str, tech_area: str):
    hashed_password = generate_password_hash(password)
    user = User(username=username, password_hash=hashed_password, tech_area=tech_area)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def get_desks_by_floor(db: Session, floor: str):
    return db.query(Desk).filter(Desk.floor == floor).all()

def update_desk_status(db: Session, desk_id: str, status: str, user_id: int = None):
    desk = db.query(Desk).filter(Desk.desk_id == desk_id).first()
    if desk:
        desk.status = status
        desk.user_id = user_id if status == "occupied" else None
        db.commit()
        return desk
    return None

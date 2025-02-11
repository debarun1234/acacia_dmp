from sqlalchemy.orm import Session
from models import User, Desk
from werkzeug.security import generate_password_hash, check_password_hash

# -------------------- 🟢 USER CRUD OPERATIONS --------------------

def get_user_by_username(db: Session, username: str):
    """Retrieve a user by their username."""
    return db.query(User).filter(User.username == username).first()

def get_user_by_id(db: Session, user_id: int):
    """Retrieve a user by their ID."""
    return db.query(User).filter(User.id == user_id).first()

def create_user(db: Session, username: str, password: str, tech_area: str, role="user"):
    """Create a new user with hashed password."""
    hashed_password = generate_password_hash(password)
    user = User(username=username, password_hash=hashed_password, tech_area=tech_area, role=role)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def update_user_password(db: Session, user_id: int, new_password: str):
    """Update a user's password."""
    user = get_user_by_id(db, user_id)
    if user:
        user.password_hash = generate_password_hash(new_password)
        db.commit()
        return True
    return False

def update_user_tech_area(db: Session, user_id: int, new_tech_area: str):
    """Update a user's tech area."""
    user = get_user_by_id(db, user_id)
    if user:
        user.tech_area = new_tech_area
        db.commit()
        return True
    return False

def delete_user(db: Session, user_id: int):
    """Delete a user from the database."""
    user = get_user_by_id(db, user_id)
    if user:
        db.delete(user)
        db.commit()
        return True
    return False

def get_users_by_tech_area(db: Session, tech_area: str):
    """Retrieve all users belonging to a specific tech area."""
    return db.query(User).filter(User.tech_area == tech_area).all()

# -------------------- 🔵 DESK CRUD OPERATIONS --------------------

def get_desks_by_floor(db: Session, floor: str):
    """Retrieve all desks for a given floor."""
    return db.query(Desk).filter(Desk.floor == floor).all()

def get_desks_by_tech_area(db: Session, tech_area: str):
    """Retrieve all desks for a given tech area."""
    return db.query(Desk).filter(Desk.tech_area == tech_area).all()

def update_desk_status(db: Session, desk_id: str, status: str, user_id: int = None):
    """Update the status of a desk (available/occupied)."""
    desk = db.query(Desk).filter(Desk.desk_id == desk_id).first()
    if desk:
        desk.status = status
        desk.user_id = user_id if status == "occupied" else None
        db.commit()
        return desk
    return None

def reset_all_desks_on_floor(db: Session, floor: str):
    """Reset all desks on a given floor to available status."""
    desks = db.query(Desk).filter(Desk.floor == floor).all()
    for desk in desks:
        desk.status = "available"
        desk.user_id = None
    db.commit()
    return True

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database import Base
from werkzeug.security import generate_password_hash, check_password_hash

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)
    role = Column(String, default="user")  # "admin" or "user"
    tech_area = Column(String, nullable=False)  # Restrict seat booking

    def set_password(self, password: str):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password: str):
        return check_password_hash(self.password_hash, password)

    # 🔹 Fix: Ensure correct back_populates reference
    desks = relationship("Desk", back_populates="assigned_user")

class Desk(Base):
    __tablename__ = "desks"

    id = Column(Integer, primary_key=True, index=True)
    desk_id = Column(String, unique=True, nullable=False)
    floor = Column(String, nullable=False)  # Floor number (L1, L2, L3, etc.)
    status = Column(String, default="available")  # "available" or "occupied"
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    tech_area = Column(String, nullable=False)  # Ensures users only book in their area

    # 🔹 Fix: Use matching back_populates reference
    assigned_user = relationship("User", back_populates="desks")

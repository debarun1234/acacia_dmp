import json
from sqlalchemy.orm import Session
from database import SessionLocal
from models import Desk, User

def load_json_to_db():
    db: Session = SessionLocal()

    # Load JSON file
    with open("..\\data\\L2.json", "r") as f:
        data = json.load(f)

    # Insert desks into database
    for desk_id, details in data["desks"].items():
        user = None

        # If a user is present, find their ID
        if details["user"]:
            user = db.query(User).filter(User.username == details["user"]).first()
            if not user:
                print(f"⚠️ User '{details['user']}' not found in database!")

        new_desk = Desk(
            desk_id=desk_id,
            floor="L2",  # Fixed floor since we're importing L2.json
            status=details["status"],
            tech_area=details["tech_area"],
            user_id=user.id if user else None  # Assign user_id if found
        )
        db.add(new_desk)

    db.commit()
    db.close()
    print("✅ Successfully imported L2.json into the database!")

if __name__ == "__main__":
    load_json_to_db()

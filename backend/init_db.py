from database import engine, Base
from models import User, Desk  # Ensure models are imported

print("🔄 Initializing database...")

# Create tables in the database
Base.metadata.create_all(bind=engine)

print("✅ Database tables created successfully!")

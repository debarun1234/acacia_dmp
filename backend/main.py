from fastapi import FastAPI
from database import engine, Base
from auth import auth_router
from routes.desks import desk_router
from routes.users import user_router
from routes.admin import admin_router
from routes.search import search_router

app = FastAPI(title="Desk Management API")

Base.metadata.create_all(bind=engine)

app.include_router(auth_router, prefix="/auth", tags=["Authentication"])
app.include_router(user_router, prefix="/users", tags=["User Management"])
app.include_router(desk_router, prefix="/desk", tags=["Desk Management"])
app.include_router(admin_router, prefix="/admin", tags=["Admin Controls"])
app.include_router(search_router, prefix="/search", tags=["Search Functionality"])

@app.get("/")
def home():
    return {"message": "Desk Management API is running!"}

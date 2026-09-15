from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
import os
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file

# Import routers from app/routers
from routers import auth

# Create FastAPI app instance
app = FastAPI()

# Use CORS middleware to allow requests from the frontend (React app)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(
    SessionMiddleware, 
    secret_key=os.getenv("SESSION_SECRET_KEY"))  

# Include the authentication router
app.include_router(auth.router)

@app.get("/")
def root():
    return {"status": "FastAPI is running!"}
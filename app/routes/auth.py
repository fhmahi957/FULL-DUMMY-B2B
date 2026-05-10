# app/routes/auth.py
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta

from app.database import get_db
from app.utils.auth import (
    authenticate_user,
    create_access_token,
    get_password_hash,
    get_user_by_email
)
from app.models.user import User
from app.schemas.user import UserCreate, UserResponse, LoginResponse, UserInLogin
# Add this at the top of auth.py after imports
from fastapi import Response

router = APIRouter(prefix="/auth", tags=["Authentication"])


# Add an OPTIONS handler for the register endpoint
@router.options("/register")
async def register_options():
    return Response(status_code=200)

@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register(user: UserCreate, db: Session = Depends(get_db)):
    """Register a new user"""
    db_user = get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
   
    new_user = User(
        username=user.username,
        email=user.email,
        hashed_password=get_password_hash(user.password),
        role=user.role
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.post("/login", response_model=LoginResponse)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    
    """Login and receive JWT token with user info"""
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
   
    # Create access token with role
    access_token_expires = timedelta(minutes=30)
    access_token = create_access_token(
        data={
            "sub": user.email,
            "role": user.role
        },
        expires_delta=access_token_expires
    )
    
    # Return properly typed LoginResponse model
    return LoginResponse(
        access_token=access_token,
        token_type="bearer",
        user=UserInLogin(
            name=user.username,  # Frontend expects "name"
            email=user.email,
            role=user.role
        )
    )
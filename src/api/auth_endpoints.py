from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel, EmailStr, Field, field_validator
import re
from typing import Optional

from ..database.database import get_db
from ..database.models import User
from ..auth.auth import hash_password, verify_password, create_access_token
from ..auth.dependencies import get_current_user

router = APIRouter(prefix="/auth", tags=["Authentication"])

class UserRegister(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=8)
    full_name: Optional[str] = None

    @field_validator("password")
    @classmethod
    def validate_password_strength(cls, v: str) -> str:
        if not re.search(r"[A-Z]", v):
            raise ValueError("Le mot de passe doit contenir au moins une majuscule")
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', v):
            raise ValueError("Le mot de passe doit contenir au moins un caractère spécial")
        return v

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: int
    email: str
    full_name: Optional[str]
    email_verified: bool
    is_active: bool
    created_at: str
    class Config: from_attributes = True

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserResponse

class MessageResponse(BaseModel):
    message: str

@router.post("/register", response_model=TokenResponse, status_code=status.HTTP_201_CREATED)
def register(user_data: UserRegister, db: Session = Depends(get_db)):
    from datetime import datetime
    
    existing_user = db.query(User).filter(User.email == user_data.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    new_user = User(
        email=user_data.email,
        hashed_password=hash_password(user_data.password),
        full_name=user_data.full_name,
        is_active=True,
        email_verified=True,
        privacy_policy_accepted_at=datetime.utcnow()  # GDPR: Record consent timestamp
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    access_token = create_access_token(data={"sub": new_user.email})
    return TokenResponse(
        access_token=access_token,
        user=UserResponse(
            id=new_user.id, 
            email=new_user.email, 
            full_name=new_user.full_name, 
            email_verified=new_user.email_verified,
            is_active=new_user.is_active,
            created_at=new_user.created_at.isoformat()
        )
    )

@router.post("/login", response_model=TokenResponse)
def login(credentials: UserLogin, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == credentials.email).first()
    if not user or not verify_password(credentials.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Email ou mot de passe incorrect")
    
    access_token = create_access_token(data={"sub": user.email})
    return TokenResponse(
        access_token=access_token,
        user=UserResponse(
            id=user.id, 
            email=user.email, 
            full_name=user.full_name, 
            email_verified=user.email_verified,
            is_active=user.is_active,
            created_at=user.created_at.isoformat()
        )
    )

@router.get("/me", response_model=UserResponse)
def get_current_user_info(current_user: User = Depends(get_current_user)):
    """Get current authenticated user information."""
    return UserResponse(
        id=current_user.id,
        email=current_user.email,
        full_name=current_user.full_name,
        email_verified=current_user.email_verified,
        is_active=current_user.is_active,
        created_at=current_user.created_at.isoformat()
    )


@router.get("/me", response_model=UserResponse)
def get_me(current_user: User = Depends(get_current_user)):
    return UserResponse(
        id=current_user.id, 
        email=current_user.email, 
        full_name=current_user.full_name, 
        email_verified=current_user.email_verified,
        is_active=current_user.is_active,
        created_at=current_user.created_at.isoformat()
    )

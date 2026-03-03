from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel, EmailStr, Field, field_validator
import re
from typing import Optional

from ..database.database import get_db
from ..database.models import User, AuthToken
from ..auth.auth import hash_password, verify_password, create_access_token
from ..auth.dependencies import get_current_user
from ..utils.email_service import send_verification_email, send_reset_password_email
from uuid import uuid4
from datetime import datetime, timedelta

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

class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    full_name: Optional[str] = None
    current_password: Optional[str] = None
    new_password: Optional[str] = Field(None, min_length=8)

    @field_validator("new_password")
    @classmethod
    def validate_new_password_strength(cls, v: Optional[str]) -> Optional[str]:
        if v is None:
            return v
        if len(v) < 8:
            raise ValueError("Le mot de passe doit contenir au moins 8 caractères")
        if not re.search(r"[A-Z]", v):
            raise ValueError("Le mot de passe doit contenir au moins une majuscule")
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', v):
            raise ValueError("Le mot de passe doit contenir au moins un caractère spécial")
        return v

class ForgotPasswordRequest(BaseModel):
    email: EmailStr

class ResetPasswordRequest(BaseModel):
    token: str
    new_password: str = Field(..., min_length=8)

    @field_validator("new_password")
    @classmethod
    def validate_reset_password_strength(cls, v: str) -> str:
        if not re.search(r"[A-Z]", v):
            raise ValueError("Le mot de passe doit contenir au moins une majuscule")
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', v):
            raise ValueError("Le mot de passe doit contenir au moins un caractère spécial")
        return v

@router.post("/register", response_model=MessageResponse, status_code=status.HTTP_201_CREATED)
def register(user_data: UserRegister, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.email == user_data.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Cet email est déjà utilisé")
    
    new_user = User(
        email=user_data.email,
        hashed_password=hash_password(user_data.password),
        full_name=user_data.full_name,
        is_active=False,      # Account inactive until email verified
        email_verified=False, # Email not verified yet
        privacy_policy_accepted_at=datetime.utcnow()
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    # Generate verification token
    token_str = uuid4().hex
    verify_token = AuthToken(
        user_id=new_user.id,
        token=token_str,
        type="verify",
        expires_at=datetime.utcnow() + timedelta(hours=24)
    )
    db.add(verify_token)
    db.commit()
    
    # Send email
    send_verification_email(new_user.email, token_str, new_user.full_name or "")
    
    return MessageResponse(message="Compte créé ! Veuillez vérifier vos emails pour l'activer.")

@router.post("/login", response_model=TokenResponse)
def login(credentials: UserLogin, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == credentials.email).first()
    if not user or not verify_password(credentials.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Email ou mot de passe incorrect")
    
    if not user.is_active:
        raise HTTPException(
            status_code=403, 
            detail="Votre compte n'est pas encore activé. Veuillez vérifier vos emails."
        )
    
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

@router.get("/verify-email", response_model=MessageResponse)
def verify_email(token: str, db: Session = Depends(get_db)):
    auth_token = db.query(AuthToken).filter(
        AuthToken.token == token,
        AuthToken.type == "verify",
        AuthToken.expires_at > datetime.utcnow()
    ).first()
    
    if not auth_token:
        raise HTTPException(status_code=400, detail="Token invalide ou expiré")
    
    user = db.query(User).get(auth_token.user_id)
    if user:
        user.is_active = True
        user.email_verified = True
        
        # Delete the token
        db.delete(auth_token)
        db.commit()
        return MessageResponse(message="Votre compte a été activé avec succès !")
    
    raise HTTPException(status_code=400, detail="Utilisateur non trouvé")

@router.post("/forgot-password", response_model=MessageResponse)
def forgot_password(data: ForgotPasswordRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == data.email).first()
    
    # Security: Always return success message even if email doesn't exist
    if user:
        # Invalidate old reset tokens
        db.query(AuthToken).filter(
            AuthToken.user_id == user.id,
            AuthToken.type == "reset"
        ).delete()
        
        # Generate new reset token
        token_str = uuid4().hex
        reset_token = AuthToken(
            user_id=user.id,
            token=token_str,
            type="reset",
            expires_at=datetime.utcnow() + timedelta(hours=1)
        )
        db.add(reset_token)
        db.commit()
        
        # Send email
        send_reset_password_email(user.email, token_str)
    
    return MessageResponse(message="Si cet email existe, un lien de réinitialisation a été envoyé.")

@router.post("/reset-password", response_model=MessageResponse)
def reset_password(data: ResetPasswordRequest, db: Session = Depends(get_db)):
    auth_token = db.query(AuthToken).filter(
        AuthToken.token == data.token,
        AuthToken.type == "reset",
        AuthToken.expires_at > datetime.utcnow()
    ).first()
    
    if not auth_token:
        raise HTTPException(status_code=400, detail="Lien de réinitialisation invalide ou expiré")
    
    user = db.query(User).get(auth_token.user_id)
    if user:
        user.hashed_password = hash_password(data.new_password)
        
        # Delete ALL reset tokens for this user
        db.query(AuthToken).filter(
            AuthToken.user_id == user.id,
            AuthToken.type == "reset"
        ).delete()
        
        db.commit()
        return MessageResponse(message="Votre mot de passe a été réinitialisé avec succès.")
    
    raise HTTPException(status_code=400, detail="Utilisateur non trouvé")

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

@router.patch("/me", response_model=UserResponse)
def update_me(
    update_data: UserUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Mettre à jour les informations de l'utilisateur connecté."""
    # Mise à jour du nom complet
    if update_data.full_name is not None:
        current_user.full_name = update_data.full_name
    
    # Mise à jour de l'email
    if update_data.email is not None and update_data.email != current_user.email:
        # Vérifier si l'email est déjà pris
        existing_user = db.query(User).filter(User.email == update_data.email).first()
        if existing_user:
            raise HTTPException(status_code=400, detail="Cet email est déjà utilisé")
        current_user.email = update_data.email
    
    # Mise à jour du mot de passe
    if update_data.new_password:
        if not update_data.current_password:
            raise HTTPException(
                status_code=400, 
                detail="Le mot de passe actuel est requis pour changer le mot de passe"
            )
        
        # 1. Vérifier le mot de passe actuel (Security)
        if not verify_password(update_data.current_password, current_user.hashed_password):
            raise HTTPException(status_code=400, detail="Mot de passe actuel incorrect")
        
        # 2. Vérifier que le nouveau est différent de l'actuel
        if verify_password(update_data.new_password, current_user.hashed_password):
            raise HTTPException(
                status_code=400, 
                detail="Le nouveau mot de passe ne peut pas être identique à l'ancien"
            )
        
        current_user.hashed_password = hash_password(update_data.new_password)
    
    db.commit()
    db.refresh(current_user)
    
    return UserResponse(
        id=current_user.id,
        email=current_user.email,
        full_name=current_user.full_name,
        email_verified=current_user.email_verified,
        is_active=current_user.is_active,
        created_at=current_user.created_at.isoformat()
    )


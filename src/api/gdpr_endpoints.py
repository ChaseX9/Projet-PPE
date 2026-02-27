"""GDPR-compliant endpoints for user data management."""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import datetime
from pydantic import BaseModel
from typing import Dict, Any, Optional

from ..database.database import get_db
from ..database import models
from ..auth.dependencies import get_current_user
from ..auth.auth import verify_password

router = APIRouter(prefix="/api/user", tags=["gdpr"])


class ConsentUpdate(BaseModel):
    """Model for updating user consents."""
    cookies_consent: Optional[bool] = None
    marketing_consent: Optional[bool] = None


class AccountDeletion(BaseModel):
    """Model for account deletion confirmation."""
    password: str
    confirm_deletion: bool = False


@router.get("/data")
async def export_user_data(
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """
    Export all user data in machine-readable format (GDPR Article 20 - Data Portability).
    
    Returns complete user data including:
    - Profile information
    - Investment profiles and questionnaires
    - Portfolio history
    - Academy progress
    - Consent records
    """
    # Fetch all related data
    profiles = db.query(models.SavedProfile).filter(
        models.SavedProfile.user_id == current_user.id
    ).all()
    
    portfolios = db.query(models.SavedPortfolio).filter(
        models.SavedPortfolio.user_id == current_user.id
    ).all()
    
    # Training stats and completed lessons
    training_stats = db.query(models.UserTrainingStats).filter(
        models.UserTrainingStats.user_id == current_user.id
    ).first()
    
    completed_progress = db.query(models.UserLessonProgress).filter(
        models.UserLessonProgress.user_id == current_user.id,
        models.UserLessonProgress.status == "completed"
    ).all()
    completed_lesson_ids = [lp.lesson_id for lp in completed_progress]
    
    # Compile complete data export
    export_data = {
        "export_date": datetime.utcnow().isoformat(),
        "user_account": {
            "id": current_user.id,
            "email": current_user.email,
            "full_name": current_user.full_name,
            "created_at": current_user.created_at.isoformat() if current_user.created_at else None,
            "email_verified": current_user.email_verified,
            "is_active": current_user.is_active,
        },
        "gdpr_consents": {
            "privacy_policy_accepted_at": current_user.privacy_policy_accepted_at.isoformat() if current_user.privacy_policy_accepted_at else None,
            "cookies_consent": current_user.cookies_consent,
            "marketing_consent": current_user.marketing_consent,
        },
        "investment_profiles": [
            {
                "id": p.id,
                "created_at": p.created_at.isoformat() if p.created_at else None,
                "risk_profile": p.risk_profile,
                "risk_score": p.risk_score,
                "horizon_score": p.horizon_score,
                "expertise_level": p.expertise_level,
                "confidence_score": p.confidence_score,
                "questionnaire_data": p.questionnaire_data,
                "coherence_flags": p.coherence_flags,
            }
            for p in profiles
        ],
        "portfolios": [
            {
                "id": ptf.id,
                "created_at": ptf.created_at.isoformat() if ptf.created_at else None,
                "status": ptf.status,
                "optimization_method": ptf.optimization_method,
                "expected_return": ptf.expected_return,
                "volatility": ptf.volatility,
                "sharpe_ratio": ptf.sharpe_ratio,
                "total_positions": ptf.total_positions,
                "positions": ptf.positions,
                "category_allocations": ptf.category_allocations,
            }
            for ptf in portfolios
        ],
        "academy_progress": {
            "total_xp": training_stats.total_xp if training_stats else 0,
            "completed_lessons": completed_lesson_ids,
            "current_streak": training_stats.current_streak if training_stats else 0,
            "longest_streak": training_stats.longest_streak if training_stats else 0,
            "last_activity": training_stats.last_activity_date.isoformat() if training_stats and training_stats.last_activity_date else None,
        } if training_stats else None,
    }
    
    return export_data


@router.delete("/account")
async def delete_user_account(
    deletion_request: AccountDeletion,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Permanently delete user account and all associated data (GDPR Article 17 - Right to Erasure).
    
    This action:
    - Deletes user profile
    - Deletes all investment profiles and questionnaires
    - Deletes all portfolios
    - Deletes Academy progress
    - Cannot be undone
    """
    # Verify password for security
    if not verify_password(deletion_request.password, current_user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect password"
        )
    
    # Require explicit confirmation
    if not deletion_request.confirm_deletion:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You must confirm account deletion"
        )
    
    # Delete all related data explicitly
    db.query(models.UserLessonProgress).filter(
        models.UserLessonProgress.user_id == current_user.id
    ).delete()

    db.query(models.UserTrainingStats).filter(
        models.UserTrainingStats.user_id == current_user.id
    ).delete()

    db.query(models.SavedPortfolio).filter(
        models.SavedPortfolio.user_id == current_user.id
    ).delete()

    db.query(models.SavedProfile).filter(
        models.SavedProfile.user_id == current_user.id
    ).delete()

    # Finally, delete the user account
    db.delete(current_user)
    db.commit()
    
    return {
        "message": "Your account and all associated data have been permanently deleted",
        "deleted_at": datetime.utcnow().isoformat()
    }


@router.post("/consent")
async def update_consent(
    consent_update: ConsentUpdate,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update user consent preferences (GDPR Article 7 - Consent)."""
    if consent_update.cookies_consent is not None:
        current_user.cookies_consent = consent_update.cookies_consent
    
    if consent_update.marketing_consent is not None:
        current_user.marketing_consent = consent_update.marketing_consent
    
    db.commit()
    
    return {
        "message": "Consent preferences updated successfully",
        "cookies_consent": current_user.cookies_consent,
        "marketing_consent": current_user.marketing_consent,
    }


@router.get("/consent")
async def get_consent(
    current_user: models.User = Depends(get_current_user)
):
    """Retrieve current consent preferences."""
    return {
        "privacy_policy_accepted_at": current_user.privacy_policy_accepted_at.isoformat() if current_user.privacy_policy_accepted_at else None,
        "cookies_consent": current_user.cookies_consent,
        "marketing_consent": current_user.marketing_consent,
    }

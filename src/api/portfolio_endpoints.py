"""Endpoints for managing saved portfolios."""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional

from ..database.database import get_db
from ..database.models import User, SavedPortfolio, SavedProfile
from ..auth.dependencies import get_current_user, get_verified_user
from .models import PortfolioDetailResponse, ProfileSummary, PortfolioSummary, PortfolioPosition

router = APIRouter(prefix="/api/portfolios", tags=["Portfolios"])

@router.get("/")
def get_portfolios(
    limit: int = 10, 
    offset: int = 0, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """List all portfolios for current user."""
    portfolios = db.query(SavedPortfolio).filter(
        SavedPortfolio.user_id == current_user.id,
        SavedPortfolio.status == "accepted"
    ).order_by(SavedPortfolio.created_at.desc()).offset(offset).limit(limit).all()
    
    return portfolios

@router.get("/{portfolio_id}", response_model=PortfolioDetailResponse)
def get_portfolio(
    portfolio_id: int, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get details of a specific portfolio."""
    portfolio = db.query(SavedPortfolio).filter(
        SavedPortfolio.id == portfolio_id,
        SavedPortfolio.user_id == current_user.id
    ).first()
    
    if not portfolio:
        raise HTTPException(status_code=404, detail="Portfolio not found")
    
    profile = portfolio.profile
    if not profile:
         raise HTTPException(status_code=404, detail="Associated profile not found")

    # Format response
    return PortfolioDetailResponse(
        id=portfolio.id,
        created_at=portfolio.created_at.isoformat(),
        profile=ProfileSummary(
            risk_profile=profile.risk_profile,
            expertise_level=profile.expertise_level,
            risk_score=profile.risk_score,
            horizon_score=profile.horizon_score,
            confidence_score=profile.confidence_score,
            coherence_flags=profile.coherence_flags,
            explanation_level=profile.explanation_level
        ),
        portfolio=PortfolioSummary(
            positions=[PortfolioPosition(**p) for p in portfolio.positions],
            category_allocations=portfolio.category_allocations,
            expected_return=portfolio.expected_return,
            volatility=portfolio.volatility,
            sharpe_ratio=portfolio.sharpe_ratio,
            optimization_method=portfolio.optimization_method,
            total_positions=portfolio.total_positions
        )
    )

@router.delete("/{portfolio_id}")
def delete_portfolio(
    portfolio_id: int, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Delete a specific portfolio."""
    portfolio = db.query(SavedPortfolio).filter(
        SavedPortfolio.id == portfolio_id,
        SavedPortfolio.user_id == current_user.id
    ).first()
    
    if not portfolio:
        raise HTTPException(status_code=404, detail="Portfolio not found")
        
    db.delete(portfolio)
    db.commit()
    
    return {"status": "deleted"}

@router.post("/{portfolio_id}/accept")
def accept_portfolio(
    portfolio_id: int, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_verified_user)
):
    """Mark a portfolio as accepted by the user. Only one portfolio can be accepted at a time."""
    portfolio = db.query(SavedPortfolio).filter(
        SavedPortfolio.id == portfolio_id,
        SavedPortfolio.user_id == current_user.id
    ).first()
    
    if not portfolio:
        raise HTTPException(status_code=404, detail="Portfolio not found")
    
    # Demote any currently accepted portfolio to "alternative"
    db.query(SavedPortfolio).filter(
        SavedPortfolio.user_id == current_user.id,
        SavedPortfolio.status == "accepted"
    ).update({"status": "alternative"})
    
    # Mark this portfolio as accepted
    portfolio.status = "accepted"
    db.commit()
    
    return {"status": "accepted", "portfolio_id": portfolio_id}

@router.post("/{portfolio_id}/reject")
def reject_portfolio(
    portfolio_id: int, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_verified_user)
):
    """Mark a portfolio as rejected by the user."""
    portfolio = db.query(SavedPortfolio).filter(
        SavedPortfolio.id == portfolio_id,
        SavedPortfolio.user_id == current_user.id
    ).first()
    
    if not portfolio:
        raise HTTPException(status_code=404, detail="Portfolio not found")
    
    portfolio.status = "rejected"
    db.commit()
    
    return {"status": "rejected", "portfolio_id": portfolio_id}

@router.get("/current")
def get_current_portfolio(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get the currently accepted portfolio for the user."""
    portfolio = db.query(SavedPortfolio).filter(
        SavedPortfolio.user_id == current_user.id,
        SavedPortfolio.status == "accepted"
    ).order_by(SavedPortfolio.created_at.desc()).first()
    
    if not portfolio:
        return {"status": "none", "message": "Aucun portefeuille accepté"}
    
    profile = portfolio.profile
    if not profile:
        return {"status": "none", "message": "Profil associé introuvable"}

    # Format response
    return PortfolioDetailResponse(
        id=portfolio.id,
        created_at=portfolio.created_at.isoformat(),
        profile=ProfileSummary(
            risk_profile=profile.risk_profile,
            expertise_level=profile.expertise_level,
            risk_score=profile.risk_score,
            horizon_score=profile.horizon_score,
            confidence_score=profile.confidence_score,
            coherence_flags=profile.coherence_flags,
            explanation_level=profile.explanation_level
        ),
        portfolio=PortfolioSummary(
            positions=[PortfolioPosition(**p) for p in portfolio.positions],
            category_allocations=portfolio.category_allocations,
            expected_return=portfolio.expected_return,
            volatility=portfolio.volatility,
            sharpe_ratio=portfolio.sharpe_ratio,
            optimization_method=portfolio.optimization_method,
            total_positions=portfolio.total_positions
        )
    )

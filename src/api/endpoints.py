"""Main recommendation endpoints."""
from fastapi import APIRouter, HTTPException, status, Depends
from typing import Dict, Optional, List
from sqlalchemy.orm import Session

from .models import (
    RecommendationRequest, RecommendationResponse, 
    ProfileSummary, PortfolioSummary, PortfolioPosition,
    ExplorerAsset
)
from ..profile.schemas import QuestionnaireInput
from ..profile.profile_builder import build_raw_profile
from ..profile.profile_engine import refine_profile
from ..portfolio.recommender import build_portfolio
from ..database.database import get_db
from ..database.models import User, SavedProfile, SavedPortfolio
from ..auth.dependencies import get_optional_user, get_verified_user

router = APIRouter()

@router.get("/api/recommandation/tickers", tags=["Reference"])
def get_tickers():
    """Get list of available tickers for market views."""
    from ..data.data_loader import load_or_update_universe
    universe = load_or_update_universe()
    return universe[['ticker', 'name']].to_dict(orient='records')

@router.post("/api/recommandation", response_model=RecommendationResponse, tags=["Recommendation"])
async def get_recommendation(
    request: RecommendationRequest,
    current_user: Optional[User] = Depends(get_optional_user),
    db: Session = Depends(get_db)
):
    try:
        # 1. Input Processing
        questionnaire = QuestionnaireInput(
            investment_goal=request.investment_goal,
            horizon=request.horizon,
            risk_tolerance=request.risk_tolerance,
            loss_capacity=request.loss_capacity,
            knowledge_level=request.knowledge_level,
            experience=request.experience,
            investment_amount=request.investment_amount,
            investment_mode=request.investment_mode,
            esg_preference=request.esg_preference,
            liquidity_need=request.liquidity_need,
            use_black_litterman=request.use_black_litterman,
            # Flatten views if present
            market_views=[v.model_dump() for v in request.market_views] if request.market_views else None
        )
        
        # 2. Logic execution
        raw = build_raw_profile(questionnaire)
        refined = refine_profile(raw)
        portfolio = build_portfolio(
            refined,
            force_update_universe=request.force_universe_update,
            excluded_tickers=request.excluded_tickers or []
        )
        
        # 3. Persistence if authenticated and verified
        profile_id = None
        if current_user and current_user.email_verified:
            try:
                saved_profile = SavedProfile(
                    user_id=current_user.id,
                    questionnaire_data=questionnaire.model_dump(mode="json"),
                    risk_profile=refined.risk_profile.value,
                    risk_score=refined.risk_score,
                    horizon_score=refined.horizon_score,
                    expertise_level=refined.expertise_level.value,
                    confidence_score=refined.confidence_score,
                    coherence_flags=refined.coherence_flags,
                    explanation_level=refined.explanation_level
                )
                db.add(saved_profile)
                db.commit()
                db.refresh(saved_profile)
                
                saved_portfolio = SavedPortfolio(
                    user_id=current_user.id,
                    profile_id=saved_profile.id,
                    status="adjusted" if request.excluded_tickers else "proposed",
                    parent_portfolio_id=request.parent_portfolio_id,
                    positions=portfolio['positions'],
                    category_allocations=portfolio['category_allocations'],
                    expected_return=portfolio['expected_return'],
                    volatility=portfolio['volatility'],
                    sharpe_ratio=portfolio['sharpe_ratio'],
                    optimization_method=portfolio['optimization_method'],
                    total_positions=portfolio['total_positions'],
                    excluded_tickers=request.excluded_tickers or None
                )
                db.add(saved_portfolio)
                db.commit()
                db.refresh(saved_portfolio)
                profile_id = saved_portfolio.id
            except Exception as e:
                print(f"Warning: Failed to save to DB: {e}")

        
        # 4. Generate explanations
        from ..portfolio.explainer import explain_asset, explain_portfolio
        
        # Add explanations to each position
        for position in portfolio['positions']:
            position['explanation'] = explain_asset(position)
        
        # Generate global portfolio explanation
        portfolio_explanation = explain_portfolio(
            profile={
                'risk_profile': refined.risk_profile.value,
                'horizon': questionnaire.horizon.value,
                'goal': questionnaire.investment_goal.value
            },
            positions=portfolio['positions'],
            category_allocations=portfolio['category_allocations']
        )
                # 4. Response formatting
        profile_summary = ProfileSummary(
            risk_profile=refined.risk_profile,
            expertise_level=refined.expertise_level,
            risk_score=refined.risk_score,
            horizon_score=refined.horizon_score,
            confidence_score=refined.confidence_score,
            coherence_flags=refined.coherence_flags,
            explanation_level=refined.explanation_level,
            raw_responses=questionnaire.model_dump(mode="json")
        )
        
        positions = [PortfolioPosition(**p) for p in portfolio['positions']]
        portfolio_summary = PortfolioSummary(
            positions=positions,
            category_allocations=portfolio['category_allocations'],
            expected_return=portfolio['expected_return'],
            volatility=portfolio['volatility'],
            sharpe_ratio=portfolio['sharpe_ratio'],
            optimization_method=portfolio['optimization_method'],
            processed_views=portfolio.get('processed_views'),
            total_positions=portfolio['total_positions'],
            portfolio_explanation=portfolio_explanation
        )
        
        return RecommendationResponse(
            profile=profile_summary, 
            portfolio=portfolio_summary,
            portfolio_id=profile_id
        )

    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/api/universe/stats", tags=["Reference"])
async def get_universe_stats():
    from ..data.data_loader import load_or_update_universe
    universe = load_or_update_universe()
    return {
        "total_assets": len(universe),
        "by_type": universe['asset_type'].value_counts().to_dict(),
        "avg_volatility": float(universe['volatility'].mean())
    }

@router.post("/api/recommandation/alternative", response_model=RecommendationResponse, tags=["Recommendation"])
async def get_alternative_recommendation(
    portfolio_id: int,
    current_user: User = Depends(get_verified_user),
    db: Session = Depends(get_db)
):
    """Generate an alternative portfolio based on the same profile (deterministic variation)."""
    # Retrieve original portfolio
    original = db.query(SavedPortfolio).filter(SavedPortfolio.id == portfolio_id).first()
    
    if not original:
        raise HTTPException(status_code=404, detail="Original portfolio not found")
    
    # Get the original profile  
    profile = original.profile
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    
    # Reconstruct refined profile from saved data
    from ..profile.schemas import RefinedProfile, RawProfile, QuestionnaireInput
    
    # Create questionnaire from saved data
    qi_data = profile.questionnaire_data
    qi = QuestionnaireInput(**qi_data)
    
    raw = RawProfile(
        risk_score=profile.risk_score,
        horizon_score=profile.horizon_score,
        expertise_level=profile.expertise_level,
        constraints=[],
        raw_responses=qi
    )
    
    refined_profile = RefinedProfile(
        risk_profile=profile.risk_profile,
        expertise_level=profile.expertise_level,
        risk_score=profile.risk_score,
        horizon_score=profile.horizon_score,
        confidence_score=profile.confidence_score,
        coherence_flags=profile.coherence_flags,
        explanation_level=profile.explanation_level,
        raw_profile=raw
    )
    
    # Generate alternative with slight variation (deterministic)
    # We adjust selection offset to get different assets but same overall strategy
    import os
    os.environ['ROBO_ALTERNATIVE_OFFSET'] = '1'
    
    try:
        portfolio = build_portfolio(refined_profile, force_update_universe=False)
    finally:
        os.environ.pop('ROBO_ALTERNATIVE_OFFSET', None)
    
    # Save alternative portfolio
    saved_profile_alt = SavedProfile(
        user_id=current_user.id if current_user else None,
        questionnaire_data=profile.questionnaire_data,
        risk_profile=profile.risk_profile,
        risk_score=profile.risk_score,
        horizon_score=profile.horizon_score,
        expertise_level=profile.expertise_level,
        confidence_score=profile.confidence_score,
        coherence_flags=profile.coherence_flags,
        explanation_level=profile.explanation_level
    )
    db.add(saved_profile_alt)
    db.flush()
    
    saved_portfolio = SavedPortfolio(
        user_id=current_user.id if current_user else None,
        profile_id=saved_profile_alt.id,
        status="alternative",
        parent_portfolio_id=portfolio_id,
        positions=portfolio['positions'],
        category_allocations=portfolio['category_allocations'],
        expected_return=portfolio['expected_return'],
        volatility=portfolio['volatility'],
        sharpe_ratio=portfolio['sharpe_ratio'],
        optimization_method=portfolio['optimization_method'],
        total_positions=portfolio['total_positions']
    )
    db.add(saved_portfolio)
    db.commit()
    db.refresh(saved_portfolio)
    
    return RecommendationResponse(
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
            positions=[PortfolioPosition(**p) for p in portfolio['positions']],
            category_allocations=portfolio['category_allocations'],
            expected_return=portfolio['expected_return'],
            volatility=portfolio['volatility'],
            sharpe_ratio=portfolio['sharpe_ratio'],
            optimization_method=portfolio['optimization_method'],
            processed_views=portfolio.get('processed_views'),
            total_positions=portfolio['total_positions']
        ),
        portfolio_id=saved_portfolio.id
    )

# ========== SMART SUGGESTIONS ENDPOINTS ==========

@router.get("/api/suggestion-rules", tags=["Suggestions"])
def get_suggestion_rules():
    """
    Get all suggestion rules for frontend execution.
    
    Returns:
        Dict with rules and version for audit trail
    """
    from ..profile.suggestion_rules import get_all_rules, get_rules_version, FIELD_ORDER
    
    return {
        "version": get_rules_version(),
        "rules": get_all_rules(),
        "field_order": FIELD_ORDER
    }

@router.post("/api/evaluate-suggestions", tags=["Suggestions"])
def evaluate_suggestions(responses: Dict):
    """
    Evaluate suggestions based on current questionnaire responses.
    
    This is for backend validation and testing.
    Frontend should use /api/suggestion-rules and evaluate locally.
    
    Args:
        responses: Current questionnaire responses
        
    Returns:
        Dict with suggestions and coherence score
    """
    from ..profile.suggestion_engine import evaluate_suggestions, calculate_coherence_score
    
    suggestions = evaluate_suggestions(responses)
    coherence = calculate_coherence_score(responses)
    
    return {
        "suggestions": [s.to_dict() for s in suggestions],
        "coherence": coherence
    }

# Persistent cache for explorer assets to avoid repeated heavy processing
EXPLORER_CACHE_FILE = PROJECT_ROOT / "data" / "explorer_cache.json"

async def prefetch_explorer_assets():
    """Trigger a refresh of the explorer cache. Designed to be called in background."""
    print("🔭 Prefetching Explorer assets...")
    try:
        await get_explorer_assets(force_refresh=True)
        print("✓ Explorer cache prefilled")
    except Exception as e:
        print(f"❌ Explorer prefetch failed: {e}")

@router.get("/api/explorer/assets", response_model=List[ExplorerAsset], tags=["Explorer"])
async def get_explorer_assets(force_refresh: bool = False):
    """Get all assets with pedagogical data and simplified history for the Explorer."""
    import time
    import math
    import json
    from ..data.data_loader import load_or_update_universe, get_sparklines_batch
    from ..data.pedagogy_data import get_asset_pedagogy
    
    # 1. Check persistent cache if not forcing refresh
    if not force_refresh and EXPLORER_CACHE_FILE.exists():
        try:
            # Check age (optional: here we trust the file if it exists, 
            # as it's updated in background by load_or_update_universe)
            with open(EXPLORER_CACHE_FILE, "r", encoding="utf-8") as f:
                cached_data = json.load(f)
                if cached_data:
                    return cached_data
        except Exception as e:
            print(f"⚠️ Cache read error: {e}")

    try:
        universe = load_or_update_universe()
        if universe.empty:
            return []
            
        tickers = universe['ticker'].tolist()
        
        # 2. Batch fetch sparklines
        sparklines = get_sparklines_batch(tickers)
        
        explorer_assets_dicts = []
        for _, row in universe.iterrows():
            ticker = row['ticker']
            
            vol = row['volatility']
            if math.isnan(vol): vol = 0.0
                
            if vol < 0.12: level = "Faible"
            elif vol < 0.22: level = "Modéré"
            else: level = "Élevé"
                
            asset_sparkline = sparklines.get(ticker, [])
            has_sparkline = len(asset_sparkline) > 0
            
            try:
                pedagogy = get_asset_pedagogy(ticker, row['asset_type'], row['geography'], level)
            except Exception:
                continue
            
            # Create dict for easy JSON serialization
            asset_dict = {
                "ticker": ticker,
                "name": row['name'],
                "asset_type": row['asset_type'].value if hasattr(row['asset_type'], 'value') else row['asset_type'],
                "asset_class": row['asset_class'].value if hasattr(row['asset_class'], 'value') else row['asset_class'],
                "category": row['category'].value if hasattr(row['category'], 'value') else row['category'],
                "geography": row['geography'],
                "sector": row.get('sector'),
                "volatility_level": level,
                "volatility_score": round(vol, 4),
                "is_esg": bool(row['is_esg']),
                "pedagogy_short": pedagogy['pedagogy_short'],
                "pedagogy_long": pedagogy['pedagogy_long'],
                "utility": pedagogy['utility'],
                "why_capinvest": pedagogy['why_capinvest'],
                "suitable_profiles": pedagogy['suitable_profiles'],
                "key_takeaways": pedagogy['key_takeaways'],
                "sparkline": asset_sparkline,
                "has_sparkline": has_sparkline
            }
            explorer_assets_dicts.append(asset_dict)
            
        # 3. Update persistent cache
        try:
            EXPLORER_CACHE_FILE.parent.mkdir(parents=True, exist_ok=True)
            with open(EXPLORER_CACHE_FILE, "w", encoding="utf-8") as f:
                json.dump(explorer_assets_dicts, f, ensure_ascii=False, indent=2)
            print(f"✓ Persistent cache updated with {len(explorer_assets_dicts)} assets")
        except Exception as e:
            print(f"⚠️ Cache write error: {e}")
            
        return explorer_assets_dicts
        
    except Exception as e:
        print(f"CRITICAL ERROR in get_explorer_assets: {e}")
        raise HTTPException(status_code=500, detail=str(e))

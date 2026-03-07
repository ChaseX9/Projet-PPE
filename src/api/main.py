"""FastAPI application - Main entry point."""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pathlib import Path
import uvicorn

from .endpoints import router, prefetch_explorer_assets
from .auth_endpoints import router as auth_router
from .portfolio_endpoints import router as portfolio_router
from .training_endpoints import router as training_router
from .gdpr_endpoints import router as gdpr_router
from .models import HealthCheckResponse
from ..utils.config import API_TITLE, API_DESCRIPTION, API_VERSION, PROJECT_ROOT, UNIVERSE_FILE
from ..data.storage import get_universe_age

app = FastAPI(title=API_TITLE, description=API_DESCRIPTION, version=API_VERSION)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files
static_dir = PROJECT_ROOT / "static"
app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")

# Include routers
app.include_router(router)
app.include_router(auth_router)
app.include_router(portfolio_router)
app.include_router(training_router)
app.include_router(gdpr_router)

@app.on_event("startup")
async def startup_event():
    from ..database.database import init_db, SessionLocal
    from ..database.seeding import auto_seed_or_update
    from ..data.data_loader import load_or_update_universe
    import os
    import threading
    
    # 1. Immediate initialization (lightweight)
    try:
        init_db()
        print("✓ Database structure initialized")
    except Exception as e:
        print(f"❌ Database init error: {e}")

    # 2. Log SMTP Configuration (for debugging Render emails)
    smtp_user = os.getenv("SMTP_USER")
    smtp_pass = os.getenv("SMTP_PASSWORD")
    if smtp_user and smtp_pass:
        print(f"✓ SMTP configured (User: {smtp_user})")
    else:
        print("⚠️ SMTP NOT configured - Emails will be stubbed in logs")

    # 3. Offload ALL heavy tasks to background thread
    def background_startup():
        print("🌱 Background startup began...")
        db = SessionLocal()
        try:
            # Seed Academy (can be slow)
            auto_seed_or_update(db)
            print("✓ Academy curriculum updated")
        except Exception as e:
            print(f"❌ Background seeding error: {e}")
        finally:
            db.close()
            
        try:
            # Fetch Financial Data (very slow: 5-10 mins for 479 assets)
            load_or_update_universe(max_age_days=2)
            print("✓ Universe data refreshed")
        except Exception as e:
            print(f"❌ Background data loading error: {e}")
            
        try:
            # Prefetch Explorer cache (heavy)
            import asyncio
            asyncio.run(prefetch_explorer_assets())
        except Exception as e:
            print(f"❌ Background explorer prefetch error: {e}")
        
        print("🚀 Background startup complete")

    threading.Thread(target=background_startup, daemon=True).start()
    print("⚡ FastAPI ready - App is now listening for Render port scan")

@app.get("/", tags=["Pages"])
async def root():
    return FileResponse(PROJECT_ROOT / "templates" / "login.html")

@app.get("/{page}.html", tags=["Pages"])
async def get_page(page: str):
    path = PROJECT_ROOT / "templates" / f"{page}.html"
    if path.exists():
        return FileResponse(path)
    return {"error": "Page not found"}

@app.get("/health", response_model=HealthCheckResponse, tags=["Health"])
async def health_check():
    age = get_universe_age(UNIVERSE_FILE)
    return HealthCheckResponse(
        status="healthy", version=API_VERSION, universe_loaded=age is not None, universe_age_days=age
    )

if __name__ == "__main__":
    uvicorn.run("src.api.main:app", host="0.0.0.0", port=8000, reload=True)

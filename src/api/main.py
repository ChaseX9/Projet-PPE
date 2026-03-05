"""FastAPI application - Main entry point."""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pathlib import Path
import uvicorn

from .endpoints import router
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
    
    try:
        init_db()
        print("✓ Database initialized")
        
        db = SessionLocal()
        try:
            auto_seed_or_update(db)
        finally:
            db.close()
            
        load_or_update_universe(max_age_days=2)
        print("✓ Universe ready")
    except Exception as e:
        print(f"Warning during startup: {e}")

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

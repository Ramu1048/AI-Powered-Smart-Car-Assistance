import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse, FileResponse
from fastapi.staticfiles import StaticFiles

from app.database.postgres import engine, Base
from app.routers.auth import router as auth_router
from app.routers.cars import router as cars_router
from app.routers.compare import router as compare_router
from app.routers.showrooms import router as showrooms_router
from app.routers.bookings import router as bookings_router
from app.routers.reviews import router as reviews_router
from app.routers.wishlist import router as wishlist_router
from app.routers.admin import router as admin_router
from app.routers.ai import router as ai_router

# Create tables automatically
try:
    Base.metadata.create_all(bind=engine)
except Exception as e:
    print(f"Warning: Table creation skipped or failed: {e}")

app = FastAPI(
    title="AI-Powered Smart Car Assistance API",
    description="Backend API for discovering, comparing, reviewing, and booking cars in showrooms.",
    version="1.0.0"
)

# CORS configurations
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register Routers
app.include_router(auth_router, prefix="/api")
app.include_router(cars_router, prefix="/api")
app.include_router(compare_router, prefix="/api")
app.include_router(showrooms_router, prefix="/api")
app.include_router(bookings_router, prefix="/api")
app.include_router(reviews_router, prefix="/api")
app.include_router(wishlist_router, prefix="/api")
app.include_router(admin_router, prefix="/api")
app.include_router(ai_router, prefix="/api")

# Mount Built React Static Files & Handle HTML5 Client Routing Fallbacks
frontend_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "frontend", "dist")

if os.path.exists(frontend_dir):
    app.mount("/assets", StaticFiles(directory=os.path.join(frontend_dir, "assets")), name="assets")
    
    # Mount car images from frontend/dist/cars/ (copied from public/cars/ during build)
    cars_dir = os.path.join(frontend_dir, "cars")
    if os.path.exists(cars_dir):
        app.mount("/cars", StaticFiles(directory=cars_dir), name="car_images")
    
    @app.get("/{catchall:path}", include_in_schema=False)
    def serve_react_app(catchall: str):
        if catchall.startswith("api") or catchall.startswith("docs") or catchall.startswith("openapi.json"):
            raise HTTPException(status_code=404, detail="Not Found")
        # Check if requesting a static file that exists on disk
        file_path = os.path.join(frontend_dir, catchall)
        if os.path.isfile(file_path):
            return FileResponse(file_path)
        return FileResponse(os.path.join(frontend_dir, "index.html"))
else:
    @app.get("/", include_in_schema=False)
    def root():
        return RedirectResponse(url="/docs")

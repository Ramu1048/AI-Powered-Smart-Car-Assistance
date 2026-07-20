from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
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

# Create Postgres tables automatically
Base.metadata.create_all(bind=engine)

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
app.include_router(auth_router)
app.include_router(cars_router)
app.include_router(compare_router)
app.include_router(showrooms_router)
app.include_router(bookings_router)
app.include_router(reviews_router)
app.include_router(wishlist_router)
app.include_router(admin_router)
app.include_router(ai_router)


@app.get("/", include_in_schema=False)
def root():
    return RedirectResponse(url="/docs")

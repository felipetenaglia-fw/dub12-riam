from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database import init_db, engine
from .config import get_settings
from .routers import auth, users, classes, tasks, musical_pieces, feedback, recordings, quizzes, performance, ai_coach
from .seed_data import seed_database

settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan context manager for startup and shutdown events."""
    # Startup: Initialize database and seed data
    print("Initializing database...")
    init_db()
    print("Seeding database...")
    seed_database(engine)
    print("Startup complete!")
    yield
    # Shutdown: cleanup if needed
    print("Shutting down...")


# Create FastAPI app
app = FastAPI(
    title=settings.app_name,
    description="API for the Royal Irish Academy of Music Learning Management System",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify allowed origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(classes.router)
app.include_router(tasks.router)
app.include_router(musical_pieces.router)
app.include_router(feedback.router)
app.include_router(recordings.router)
app.include_router(quizzes.router)
app.include_router(performance.router)
app.include_router(ai_coach.router)


@app.get("/")
def root():
    """Root endpoint."""
    return {
        "message": "Welcome to RIAM Learning Management System API",
        "version": "1.0.0",
        "docs": "/docs"
    }


@app.get("/health")
def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}

import os
from pathlib import Path
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse

from server.database import seed_database_if_needed
from server.routers import pairs, labels, export, analytics


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: ensure tables exist and seed initial prompt-response pairs if < 50
    try:
        seed_database_if_needed()
    except Exception as e:
        print(f"Startup database check/seed notice: {e}")
    yield
    # Shutdown logic if any


app = FastAPI(
    title="RLHF Preference Labeling & Data Export API",
    description="Full-stack system for collecting pairwise human preference feedback for AI alignment and reward model training.",
    version="1.0.0",
    lifespan=lifespan
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Healthcheck endpoint (Contract 1: used for docker healthcheck)
@app.get("/health", tags=["Health"])
def health_check():
    return {"status": "healthy", "service": "rlhf-preference-backend"}


# Register API Routers
app.include_router(pairs.router)
app.include_router(labels.router)
app.include_router(export.router)
app.include_router(analytics.router)

# Static file serving for SPA frontend
static_dir = Path(__file__).resolve().parent / "static"
if static_dir.exists():
    assets_dir = static_dir / "assets"
    if assets_dir.exists():
        app.mount("/assets", StaticFiles(directory=assets_dir), name="assets")

    @app.get("/{full_path:path}", include_in_schema=False)
    async def serve_spa(full_path: str):
        file_path = static_dir / full_path
        if file_path.exists() and file_path.is_file():
            return FileResponse(file_path)
        index_file = static_dir / "index.html"
        if index_file.exists():
            return FileResponse(index_file)
        return JSONResponse({"message": "RLHF Preference Labeling API is running."})
else:
    @app.get("/", include_in_schema=False)
    async def root():
        return {
            "message": "RLHF Preference Labeling API is running.",
            "documentation": "/docs",
            "health": "/health"
        }


if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run("server.main:app", host="0.0.0.0", port=port, reload=True)

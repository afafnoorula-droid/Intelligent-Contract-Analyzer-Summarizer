from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path

from app.routers.analyze import router as analyze_router
from app.utils.auth import router as auth_router
from app.utils.logger import logger

app = FastAPI(
    title="Intelligent Contract Analyzer",
    version="2.3"
)

# -----------------------------
# CORS
# -----------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -----------------------------
# Include Routers
# -----------------------------
app.include_router(analyze_router)
app.include_router(auth_router, prefix="/api/auth")

# -----------------------------
# Debug: Print Registered Routes
# -----------------------------
print("\n================ REGISTERED ROUTES ================\n")

for route in app.routes:
    methods = getattr(route, "methods", [])
    print(f"{methods} ---> {route.path}")

print("\n===================================================\n")

# -----------------------------
# Create Required Directories
# -----------------------------
for dir_name in [
    "uploads",
    "reports",
    "chroma_db",
    "logs",
    "frontend"
]:
    Path(dir_name).mkdir(exist_ok=True)

logger.info(
    "✅ Contract Analyzer Backend Started Successfully (v2.3 with Auth + Comparison)"
)

# -----------------------------
# Root Endpoint
# -----------------------------
@app.get("/")
async def root():
    return {
        "status": "running",
        "message": "Intelligent Contract Analyzer is ready"
    }

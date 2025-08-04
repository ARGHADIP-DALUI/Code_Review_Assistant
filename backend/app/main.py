from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
import os

from app.api.v1.endpoints import submit_code  # Endpoint for /review
from app.api.v1.endpoints import style_analysis  # Endpoint for /style-check

app = FastAPI(title="Code Review Assistant")

# ✅ CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Root route
@app.get("/")
def read_root():
    return {"message": "Welcome to Code Review Assistant!"}

# ✅ Favicon route
@app.get("/favicon.ico")
def favicon():
    favicon_path = os.path.join("app", "static", "favicon.ico")
    return FileResponse(favicon_path)

# ✅ Register endpoints
app.include_router(submit_code.router, prefix="/api/v1")
app.include_router(style_analysis.router, prefix="/api/v1")


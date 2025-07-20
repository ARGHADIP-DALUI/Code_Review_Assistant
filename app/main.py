from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
import os

from app.api.v1.endpoints import submit_code  # ✅ Add this
from app.core.database import init_db         # ✅ Add DB initializer

app = FastAPI(title="Code Review Assistant")

# CORS settings
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Welcome to Code Review Assistant!"}

@app.get("/favicon.ico")
def favicon():
    favicon_path = os.path.join("app", "static", "favicon.ico")
    return FileResponse(favicon_path)

# ✅ Mount the API endpoints
app.include_router(submit_code.router, prefix="/api/v1")

# ✅ Initialize DB at startup
@app.on_event("startup")
def startup_event():
    init_db()

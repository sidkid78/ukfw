from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="Universal Knowledge Framework (UKFW) API",
    description="API for managing and querying the 13-Axis Knowledge Graph.",
    version="0.1.0",
)

# CORS configuration
origins = [
    "http://localhost:3000",
    "http://localhost:3001",
    "http://localhost:3002",
    # Add any other origins you need (e.g., your deployed frontend URL)
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"], # Allows all methods
    allow_headers=["*"], # Allows all headers
)

@app.get("/")
async def read_root():
    return {"message": "Welcome to the UKFW API"}

from .api import router
app.include_router(router)

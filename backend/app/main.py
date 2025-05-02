from fastapi import FastAPI

app = FastAPI(
    title="Universal Knowledge Framework (UKFW) API",
    description="API for managing and querying the 13-Axis Knowledge Graph.",
    version="0.1.0",
)

@app.get("/")
async def read_root():
    return {"message": "Welcome to the UKFW API"}

from .api import router
app.include_router(router)

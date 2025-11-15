from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import JSONResponse

from .routers import products, customers
from .telemetry import configure_telemetry

# app
app = FastAPI(title="Mini Store API", version="0.1.0")

# dev-friendly CORS (tighten later)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# health
@app.get("/health")
def health():
    return {"status": "ok"}

# routes
app.include_router(products.router, prefix="/products", tags=["products"])
app.include_router(customers.router, prefix="/customers", tags=["customers"])

# 404
@app.exception_handler(404)
async def not_found(_, __):
    return JSONResponse(status_code=404, content={"detail": "Not Found"})

# telemetry hook (no-op locally)
configure_telemetry(app)

# dev only: creates tables if missing 
from .database import engine
from .models import Base
Base.metadata.create_all(bind=engine)

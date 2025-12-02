from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import Base, engine
from app.routers import products, users, cart, orders

Base.metadata.create_all(bind=engine)

app = FastAPI(title="DevOps Shop API")

@app.get("/health")
def health_check():
    return {"status": "healthy"}

origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "http://localhost:5174",
    "http://127.0.0.1:5174",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(products.router, prefix="/products", tags=["Products"])
app.include_router(users.router,    prefix="/users",    tags=["Users"])
app.include_router(cart.router,     prefix="/cart",     tags=["Cart"])
app.include_router(orders.router,   prefix="/orders",   tags=["Orders"])

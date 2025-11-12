from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.routers import products, customers, orders

app = FastAPI(title="Mini Store API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow frontend to access
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(products.router)
app.include_router(customers.router)
app.include_router(orders.router)

@app.get("/")
def health_check():
    return {"status": "ok"}

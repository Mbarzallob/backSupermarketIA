from fastapi import APIRouter
from .routers import product_router

router = APIRouter()
router.include_router(product_router, prefix="/products", tags=["products"])

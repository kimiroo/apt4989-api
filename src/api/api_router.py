from fastapi import APIRouter
from api.v1 import lookup_router
from api.v1 import complex

router = APIRouter()

router.include_router(lookup_router.router)
router.include_router(complex.router)
from fastapi import APIRouter
from api.v1.lookup import phone
from api.v1.lookup import keyword
from api.v1.lookup import unit


router = APIRouter(
    prefix="/lookup",
    tags=["Lookup"]
)

router.include_router(phone.router)
router.include_router(keyword.router)
router.include_router(unit.router)

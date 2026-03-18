from fastapi import APIRouter
from api.v1 import lookup_router
from api.v1 import complexes
from api.v1 import buildings
from api.v1 import units

router = APIRouter()

router.include_router(lookup_router.router)
router.include_router(complexes.router)
router.include_router(buildings.router)
router.include_router(units.router)
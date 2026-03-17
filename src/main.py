import os

from fastapi import FastAPI, Depends

from lib.auth import verify_api_key
from api import api_router


is_dev = os.environ.get('ENV') == 'DEV'

app = FastAPI(
    title='APT4989 API',
    docs_url=None if not is_dev else "/docs",
    redoc_url=None if not is_dev else "/redoc",
    openapi_url=None if not is_dev else "/openapi.json"
)

app.include_router(
    api_router.router,
    prefix="/api/v1",
    dependencies=[Depends(verify_api_key)]
)
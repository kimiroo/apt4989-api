from fastapi import FastAPI, Depends

from lib.auth import verify_api_key
from api import api_router


app = FastAPI(title='APT4989 API')

app.include_router(
    api_router.router,
    prefix="/api/v1",
    dependencies=[Depends(verify_api_key)]
)
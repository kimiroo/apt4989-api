import os

from fastapi import Header, HTTPException, status
from typing import Annotated

API_KEY_CREDENTIAL = os.environ.get('API_KEY', '')

if not API_KEY_CREDENTIAL or len(API_KEY_CREDENTIAL) != 32:
    raise RuntimeError('Environment variable API_KEY not set or not valid length(32).')

async def verify_api_key(
        x_api_key: Annotated [
            str,
            Header(
                ...,
                alias='X-API-KEY',
                title='API 키',
                description='APT4989 API 서비스 접근을 위한 보안 토큰',
                min_length=32,
                max_length=32
            )
        ]
    ):

    if x_api_key != API_KEY_CREDENTIAL:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='Could not validate credentials'
        )
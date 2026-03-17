import os
from fastapi import HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

# Get API KEY from environment
API_KEY_CREDENTIAL = os.environ.get('API_KEY', '')

# Basic validation at startup
if not API_KEY_CREDENTIAL or len(API_KEY_CREDENTIAL) != 32:
    raise RuntimeError('Environment variable API_KEY not set or not valid length(32).')

# Initialize HTTPBearer (auto-handles 'Authorization: Bearer <token>')
reusable_oauth2 = HTTPBearer(
    scheme_name='BearerToken',
    description='APT4989 API 서비스 접근을 위한 Bearer 토큰'
)

async def verify_api_key(
    res: HTTPAuthorizationCredentials = Depends(reusable_oauth2)
):
    # res.credentials contains the actual token string
    if res.credentials != API_KEY_CREDENTIAL:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Could not validate credentials',
            headers={'WWW-Authenticate': 'Bearer'}
        )
    return res.credentials
from fastapi_jwt_auth import AuthJWT
from fastapi import Depends, status, APIRouter
from fastapi.exceptions import HTTPException

def check_authorization_token(logger,Authorize: AuthJWT = Depends()):
    try:
        Authorize.jwt_required()
        current_user = Authorize.get_jwt_subject()
        logger.info(f'Autorized success. User: {current_user}')
        return current_user

    except Exception as e:
        logger.error('Invalid token')
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail='Invalid token')


def insufficient_access_level(logger, method):
    logger.error(f'{method} request error: Insufficient access level.')
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail=f'Insufficient access level')
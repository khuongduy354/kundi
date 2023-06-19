
from typing import Annotated
from fastapi.security import OAuth2PasswordBearer
from firebase_admin import auth


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


async def parse_token(token: Annotated[str, oauth2_scheme]):
    try:
        decoded_jwt: dict = auth.verify_id_token(
            id_token=token, check_revoked=True)

        return decoded_jwt
    except:
        return None

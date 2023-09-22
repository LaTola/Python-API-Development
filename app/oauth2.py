from jose import JWTError, jwt
from datetime import datetime, timedelta
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from . import schemas
from .config import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')

# Random Key - It gets generated running
# openssl rand -hex 32
SECRET_KEY = settings.oauth_secret_key
ALGORITHM = settings.oauth_algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.oauth_token_expire


def create_access_token(data: dict) -> str:
    """
    Create an access token

    Args:
        data (dict): Data to create the token from

    Returns:
        str: The access token generated
    """
    to_encode = data.copy()
    expire = datetime.utcnow()+timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_access_token(token: str, credentials_exception) -> str:
    """
    Verifies if access token is correct

    Args:
        token (str): Access token
        credentials_exception (HTTPException): Exception raised in case of wrong credentials

    Raises:
        credentials_exception: Exception raised in case of wrong credentials
        credentials_exception: Exception raised in case of wrong credentials

    Returns:
        TokenData: Decrypted token data
    """
    try:

        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        id = payload.get("user_id")

        if not id:
            raise credentials_exception
        token_data = schemas.TokenData(id=id)
    except JWTError:
        raise credentials_exception
    except Exception as e:
        print(e)
    return token_data


def get_current_user(token: str = Depends(oauth2_scheme)):
    """
    It defines custom credentials exception and return verify_access_token result

    Args:
        token (str, optional): Encrypted token. Defaults to Depends(oauth2_scheme).

    Returns:
        TokenData: Unencrypted token
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, detail="Wrong credentials", headers={"WWW-Authenticate": "Bearer"})
    return verify_access_token(token, credentials_exception)

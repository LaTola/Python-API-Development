from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"])


def hash_password(password: str):
    """
    Encrypts the string password

    Args:
        password (str): The password to encrypt

    Returns:
        str: The encrypted password
    """
    return pwd_context.hash(password)


def verify_password(plain_pwd: str, hashed_pwd: str) -> bool:
    """
    It checks plain text password against hashed password

    Args:
        plain_pwd (str): Password in plain text
        hashed_pwd (str): Encrypted password

    Returns:
        bool: If passwords match or not
    """
    return pwd_context.verify(plain_pwd, hashed_pwd)

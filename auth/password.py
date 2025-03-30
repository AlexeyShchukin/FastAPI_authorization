from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto", bcrypt__rounds=10)


def password_hasher(password: str) -> str:
    return pwd_context.hash(password)
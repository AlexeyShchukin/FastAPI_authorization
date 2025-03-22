from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from auth.tokens import get_user_from_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")


def get_current_user_role(token: str = Depends(oauth2_scheme)) -> str:
    user = get_user_from_token(token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
        )
    return user["role"]


def has_role(required_roles: list[str]):
    def role_checker(current_role: str = Depends(get_current_user_role)):
        if current_role not in required_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You don't have permission to access this resource"
            )
        return current_role

    return role_checker

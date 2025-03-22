from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from auth.password import hash_password, pwd_context
from auth.tokens import create_access_token, create_refresh_token, get_user_from_token
from models.user import UserCreate
from database.fake_db import db, username_exists, get_user

app = FastAPI()


@app.post("/registration")
def create_user(user: UserCreate):
    if username_exists(user.username):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="A user with this name already exists",
                            )
    hashed_password = hash_password(user.password)
    db.append({"username": user.username, "password": hashed_password, "role": "user"})
    return {"message": "User registered successfully"}


@app.post("/login", description="Creating access and refresh tokens")
def login(user_data: OAuth2PasswordRequestForm = Depends()):
    user = get_user(user_data.username)
    if user and pwd_context.verify(user_data.password, user["password"]):  # Проверяем хеш пароля
        access_token = create_access_token({"sub": user_data.username})
        refresh_token = create_refresh_token({"sub": user_data.username})
        return {"access_token": access_token,
                "refresh_token": refresh_token,
                "token_type": "bearer"
                }
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                        detail="Invalid credentials",
                        headers={"WWW-Authenticate": "Bearer"},
                        )


@app.get("/refresh", description="Endpoint to refresh access token")
def refresh_token(username: str = Depends(get_user_from_token)):
    new_access_token = create_access_token({"sub": username})
    return {
        "access_token": new_access_token,
        "token_type": "bearer"
    }


@app.get("/protected", description="Endpoint for token verification")
def token_verification(username: str = Depends(get_user_from_token)):
    return username

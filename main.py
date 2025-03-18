from fastapi import FastAPI, HTTPException
from models import UserCreate
from auth import pwd_context, create_jwt_token, get_user_from_token, data_verification, get_user
from fake_db import db

app = FastAPI()


@app.post("/registration")
def create_user(user: UserCreate):
    hashed_password = data_verification(user)
    db.append({"username": user.username, "password": hashed_password})
    return {"message": f"User registered successfully"}


@app.post("/login", description="Endpoint for token creation")
def login(username: str, password: str):
    user = get_user(username)
    if user and pwd_context.verify(password, user["password"]):  # Проверяем хеш пароля
        token = create_jwt_token({"sub": username})
        return {"access_token": token}
    raise HTTPException(status_code=401, detail="Invalid credentials")


@app.get("/protected", description="Endpoint for token verification")
def token_verification(token: str):
    username = get_user_from_token(token)
    return username
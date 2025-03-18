from fastapi import FastAPI, HTTPException, status
from models import UserCreate
from auth import pwd_context, create_jwt_token, get_user_from_token

app = FastAPI()

db = [{"username": "admin", "password": "some_password"}, {"username": "some_user", "password": "some_pass"}]


def get_user(username: str):
    for user in db:
        if user.get("username") == username:
            return user
    return None


@app.post("/registration")
async def create_user(user: UserCreate):
    if any(user_data["username"] == user.username for user_data in db):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A user with this name already exists"
        )
    hashed_password = pwd_context.hash(user.password)
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
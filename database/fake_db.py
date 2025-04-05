from auth.password import get_password_hash, verify_password
from models.users import Role, UserIn, UserInDB

db = []


def save_user(user_in: UserIn):
    hashed_password = get_password_hash(user_in.password)
    user_in_db = UserInDB(**user_in.model_dump(exclude={"password"}), hashed_password=hashed_password)
    db.append(user_in_db.model_dump())
    return user_in_db


def username_exists(username: str) -> bool:
    return any(user_data["username"] == username for user_data in db)


def get_user(fake_db, username: str):
    for user in fake_db:
        if user.get("username") == username:
            return user
    return None


def authenticate_user(fake_db, username: str, password: str):
    user = get_user(fake_db, username)
    if user and verify_password(password, user.get("hashed_password")):
        return user
    return None


def create_admin():
    if not username_exists("admin"):
        hashed_password = get_password_hash("Admin_pass1")
        db.append({"username": "admin", "hashed_password": hashed_password, "role": Role.ADMIN})


create_admin()

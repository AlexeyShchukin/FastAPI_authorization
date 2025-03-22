from auth.password import hash_password

db = []


def username_exists(username: str) -> bool:
    return any(user_data["username"] == username for user_data in db)


def get_user(username: str):
    for user in db:
        if user.get("username") == username:
            return user
    return None


def create_admin():
    if not username_exists("admin"):
        hashed_password = hash_password("Admin_pass1")
        db.append({"username": "admin", "password": hashed_password, "role": "admin"})


create_admin()

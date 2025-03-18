db = [{"username": "admin", "password": "some_password"}, {"username": "some_user", "password": "some_pass"}]


def username_exists(username: str) -> bool:
    return any(user_data["username"] == username for user_data in db)


def get_user(username: str):
    for user in db:
        if user.get("username") == username:
            return user
    return None

def user_schema (user) -> dict:
    return {
        "id": str(user["_id"]),
        "username": str(user["username"]),
        "email": str(user["email"])
    }

def users_schema (users: list) -> list:
    return [user_schema(user) for user in users]

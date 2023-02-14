def user_schema_secure (user) -> dict:
    
    return {
        "id": str(user["_id"]),
        "name": str(user["name"]),
        "email": str(user["email"]),
        "role": str(user["role"]),
        "state": bool(user["state"])
    }

def user_schema (user) -> dict:

    return {
        "id": str(user["_id"]),
        "name": str(user["name"]),
        "email": str(user["email"]),
        "password": str(user["password"]),
        "role": str(user["role"]),
        "state": bool(user["state"])
    }

def users_schema (users: list) -> list:
    return [user_schema_secure(user) for user in users]
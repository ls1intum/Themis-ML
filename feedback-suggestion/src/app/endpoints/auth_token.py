def get_auth_token(authorization_header: str) -> str:
    if authorization_header is None:
        raise ValueError("Authorization header must be set")
    if not authorization_header.startswith("Bearer "):
        raise ValueError("Authorization header must start with 'Bearer '")
    return authorization_header.split(" ")[1]

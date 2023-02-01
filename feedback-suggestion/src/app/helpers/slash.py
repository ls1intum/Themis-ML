def ensure_leading_slash(s: str) -> str:
    if s.startswith("/"):
        return s
    return "/" + s

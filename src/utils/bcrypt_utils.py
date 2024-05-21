import bcrypt


def hash_password(password: str) -> str:
    """Hashea una contraseña utilizando bcrypt."""
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode("utf-8"), salt)
    return hashed_password.decode("utf-8")


def verify_password(password: str, hashed_password: str) -> bool:
    """Verifica si una contraseña coincide con un hash dado."""
    return bcrypt.checkpw(password.encode("utf-8"), hashed_password.encode("utf-8"))

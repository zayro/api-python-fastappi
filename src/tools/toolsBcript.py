import bcrypt


def createPasswd(passwd: str) -> str:
    salt = bcrypt.gensalt()
    password = bcrypt.hashpw(bytes(passwd, "utf-8"), salt)
    return str(password.decode("utf-8"))


def checkPasswd(passwd: str, hashPass: str) -> bool:
    if bcrypt.checkpw(bytes(passwd, "utf-8"), bytes(hashPass, "utf-8")):
        return True
    else:
        return False

import bcrypt


def createPasswd(passwd: str):
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(bytes(passwd, "utf-8"), salt)


def checkPasswd(passwd, hash):
    if bcrypt.checkpw(bytes(passwd, "utf-8"), bytes(hash, "utf-8")):
        return True
    else:
        return False

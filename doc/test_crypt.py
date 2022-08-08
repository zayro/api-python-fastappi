import bcrypt


passwd = b'123456'
hash = b'$2b$04$NVqY1JMfYhGSTXPGdyJFnu8FJr3NELOvo6WPW7OkJ0lfP8D6mIvbu'


salt = bcrypt.gensalt()
print(salt)
hashed = bcrypt.hashpw(passwd, salt)

print(hashed)

if bcrypt.checkpw(passwd, hash):
    print("match")
else:
    print("does not match")
import os
import dotenv
import jwt
from datetime import datetime, timedelta

dotenv.load_dotenv()


def expire_date(days: int):
    date = datetime.now()
    new_date = date + timedelta(days)
    return new_date

def write_token(data: dict):
    token = jwt.encode(payload={**data, "exp": expire_date(2) }, key=os.getenv("SECRET"), algorithm="HS256")
    return token


 
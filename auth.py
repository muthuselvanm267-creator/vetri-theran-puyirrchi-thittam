import os
from datetime import datetime, timedelta, timezone
from dotenv import load_dotenv
from fastapi import HTTPException, Request
from jose import jwt, JWTError
from passlib.context import CryptContext
from state import USERS

load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-change-me")
ALGORITHM = "HS256"
pwd = CryptContext(schemes=["bcrypt"], deprecated="auto")


def register_user(email: str, password: str):
    email = email.strip().lower()
    if email in USERS:
        raise HTTPException(400, "Account already exists")
    USERS[email] = pwd.hash(password)


def authenticate(email: str, password: str) -> bool:
    email = email.strip().lower()
    return email in USERS and pwd.verify(password, USERS[email])


def make_token(email: str):
    exp = datetime.now(timezone.utc) + timedelta(hours=12)
    return jwt.encode({"sub": email, "exp": exp}, SECRET_KEY, algorithm=ALGORITHM)


def current_user(request: Request):
    token = request.cookies.get("pocketsmart_token")
    if not token:
        return None
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload.get("sub")
    except JWTError:
        return None

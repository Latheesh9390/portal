"""
Authentication helpers: password hashing (bcrypt) and JWT issuing /
verification, for both of the portal's account types:

  - Admin accounts    (models.admin.Admin)          -> role "admin"
  - Student accounts  (models.student_account.StudentAccount) -> role "student"

Every JWT carries a `role` claim so a token issued for one role can never be
used to access routes protected for the other, even though both are signed
with the same secret.
"""

import os
import time

import bcrypt
import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from database import get_db
from models.admin import Admin
from models.student_account import StudentAccount

# In production, set ADMIN_SECRET_KEY to a long random value, e.g.:
#   export ADMIN_SECRET_KEY="$(python -c 'import secrets; print(secrets.token_hex(32))')"
SECRET_KEY = os.getenv("ADMIN_SECRET_KEY", "dev-only-insecure-secret-change-me")
ALGORITHM = "HS256"
TOKEN_TTL_SECONDS = 8 * 60 * 60  # 8 hour session, both roles


# Tells FastAPI's auto-docs where to send the "Authorize" button, and lets us
# pull the bearer token out of the Authorization header on protected routes.
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login", auto_error=False)


def hash_password(plain_password: str) -> str:
    return bcrypt.hashpw(plain_password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    try:
        return bcrypt.checkpw(plain_password.encode("utf-8"), hashed_password.encode("utf-8"))
    except ValueError:
        return False


def create_access_token(subject: str, role: str) -> str:
    """`subject` is the admin username or the student hall ticket number."""
    now = int(time.time())
    payload = {"sub": subject, "role": role, "iat": now, "exp": now + TOKEN_TTL_SECONDS}
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


def _decode_token(token: str) -> dict:
    """Returns the decoded payload ({"sub", "role", ...}), or raises HTTPException."""
    credentials_error = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid or expired session. Please log in again.",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except jwt.PyJWTError:
        raise credentials_error
    if not payload.get("sub"):
        raise credentials_error
    return payload


def get_current_admin(
    token: str | None = Depends(oauth2_scheme), db: Session = Depends(get_db)
) -> Admin:
    """FastAPI dependency: require a valid admin Bearer token. Attach this to
    every /api/admin/* route so students (who never have an admin-role
    token) get a 401."""
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    payload = _decode_token(token)
    if payload.get("role") != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Admin access required.")
    admin = db.query(Admin).filter(Admin.username == payload["sub"]).first()
    if admin is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Admin not found.")
    return admin


def get_current_student(
    token: str | None = Depends(oauth2_scheme), db: Session = Depends(get_db)
) -> StudentAccount:
    """FastAPI dependency: require a valid student Bearer token. Attach this
    to every /api/student/* route so admins (or anonymous visitors) can't
    read a student's protected "my results" data."""
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    payload = _decode_token(token)
    if payload.get("role") != "student":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Student access required.")
    account = db.query(StudentAccount).filter(StudentAccount.hallticket == payload["sub"]).first()
    if account is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Student account not found.")
    return account

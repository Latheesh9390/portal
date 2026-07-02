"""
Student authentication routes — register / login / me.

Any hall ticket number can self-register an account. If a `Student` record
already exists for that hall ticket (i.e. results have been published by the
admin), the account is linked to it and picks up the student's name
automatically. If not, the account is still created — the student simply
won't see any results until the admin publishes them under that hall ticket.
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from auth import create_access_token, get_current_student, hash_password, verify_password
from database import get_db
from models.student import Student
from models.student_account import StudentAccount
from schemas.auth import StudentLoginRequest, StudentRegisterRequest, TokenOut

router = APIRouter()


@router.post("/register", response_model=TokenOut, status_code=201)
def register(payload: StudentRegisterRequest, db: Session = Depends(get_db)):
    if payload.password != payload.confirm_password:
        raise HTTPException(status_code=400, detail="Passwords do not match.")

    hallticket = payload.hallticket  # already normalized by the schema validator

    existing = db.query(StudentAccount).filter(StudentAccount.hallticket == hallticket).first()
    if existing is not None:
        raise HTTPException(status_code=409, detail="An account already exists for this hall ticket. Please log in.")

    # Link to a published Student record if one exists yet, so the name is
    # picked up automatically. It's fine if it doesn't exist yet — the
    # account can still be created and will show results once published.
    student_record = db.query(Student).filter(Student.hallticket == hallticket).first()

    account = StudentAccount(
        hallticket=hallticket,
        student_name=student_record.student_name if student_record else None,
        hashed_password=hash_password(payload.password),
    )
    db.add(account)
    db.commit()

    token = create_access_token(hallticket, role="student")
    return TokenOut(access_token=token, username=hallticket, role="student", name=account.student_name)


@router.post("/login", response_model=TokenOut)
def login(payload: StudentLoginRequest, db: Session = Depends(get_db)):
    hallticket = payload.hallticket  # already normalized by the schema validator

    account = db.query(StudentAccount).filter(StudentAccount.hallticket == hallticket).first()
    if account is None or not verify_password(payload.password, account.hashed_password):
        raise HTTPException(status_code=401, detail="Incorrect hall ticket number or password.")

    token = create_access_token(hallticket, role="student")
    return TokenOut(access_token=token, username=hallticket, role="student", name=account.student_name)


@router.get("/me")
def me(account: StudentAccount = Depends(get_current_student)):
    return {"hallticket": account.hallticket, "name": account.student_name, "role": "student"}

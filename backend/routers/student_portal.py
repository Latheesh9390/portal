"""
Protected student-only routes. Unlike /api/results/search (public, anyone
can look up any hall ticket), these routes only ever return data for the
hall ticket tied to the logged-in student's own account.
"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from auth import get_current_student
from database import get_db
from models.student_account import StudentAccount
from routers.results import _build_regular_memo, _build_supplementary_memo

router = APIRouter()


@router.get("/me")
def student_profile(account: StudentAccount = Depends(get_current_student)):
    return {"hallticket": account.hallticket, "student_name": account.student_name}


@router.get("/my-results")
def my_results(
    exam_type: str = "regular",
    semester: str | None = None,
    account: StudentAccount = Depends(get_current_student),
    db: Session = Depends(get_db),
):
    if exam_type == "supplementary":
        memo = _build_supplementary_memo(db, account.hallticket, semester)
    else:
        memo = _build_regular_memo(db, account.hallticket, semester)

    if memo is None:
        return {
            "hallticket": account.hallticket,
            "student_name": account.student_name,
            "branch": "",
            "regulation": "",
            "batch": "",
            "photo": None,
            "results": [],
        }
    return memo

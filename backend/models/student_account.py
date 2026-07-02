"""
StudentAccount — a login account a student self-registers with, separate
from the `Student` model (which is the academic record used for the public
result search / marks memo). Any hall ticket number can create a
StudentAccount; if a matching Student record exists it's linked
automatically, otherwise results simply show empty until published.
"""

from datetime import datetime

from sqlalchemy import Column, DateTime, Integer, String

from database import Base


class StudentAccount(Base):
    __tablename__ = "student_accounts"

    id = Column(Integer, primary_key=True, index=True)
    hallticket = Column(String(30), unique=True, nullable=False, index=True)
    student_name = Column(String(200), nullable=True)
    hashed_password = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

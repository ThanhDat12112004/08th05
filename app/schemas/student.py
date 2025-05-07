from pydantic import BaseModel
from typing import Optional

class Student(BaseModel):
    studentId: str
    fullName: str
    dateOfBirth: Optional[str] = None
    gender: Optional[str] = None
    address: Optional[str] = None
    email: str
    phone: Optional[str] = None
    classId: Optional[str] = None
    accountId: Optional[str] = None

    class Config:
        from_attributes = True
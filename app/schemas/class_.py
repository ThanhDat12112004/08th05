from pydantic import BaseModel
from typing import Optional

class Class(BaseModel):
    classId: str
    className: str
    teacherId: Optional[str] = None
    facultyId: Optional[str] = None

    class Config:
        from_attributes = True
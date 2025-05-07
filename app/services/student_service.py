from datetime import datetime
from pydantic import ValidationError
from app.schemas.student import Student

async def create_student(db, student: Student):
    try:
        date_of_birth = datetime.strptime(student.dateOfBirth, '%Y-%m-%d').date() if student.dateOfBirth else None
        query = """
            INSERT INTO Students (StudentID, FullName, DateOfBirth, Gender, Address, Email, Phone, ClassID)
            VALUES ($1, $2, $3, $4, $5, $6, $7, $8)
            RETURNING *
        """
        result = await db.fetchrow(
            query,
            student.studentId,
            student.fullName,
            date_of_birth,
            student.gender,
            student.address,
            student.email,
            student.phone,
            student.classId
        )
        if result:
            return {"message": "Thêm sinh viên thành công", "data": dict(result)}
        return {"message": "Thêm sinh viên không thành công"}
    except ValidationError as ve:
        return {"message": "Dữ liệu không hợp lệ", "error": str(ve)}
    except Exception as e:
        return {"message": "Thêm sinh viên không thành công", "error": str(e)}

async def get_student(db, studentId: str):
    try:
        query = "SELECT * FROM Students WHERE StudentID = $1"
        result = await db.fetchrow(query, studentId)
        if result:
            student_data = dict(result)
            if student_data.get('DateOfBirth'):
                today = datetime.now().date()
                born = student_data['DateOfBirth']
                age = today.year - born.year - ((today.month, today.day) < (born.month, born.day))
                student_data['tuoi'] = age
            return {"data": student_data, "message": "Đã tìm thấy sinh viên"}
        return {"data": None, "message": "Không tìm thấy sinh viên"}
    except Exception as e:
        return {"data": None, "message": "Lỗi khi tìm sinh viên", "error": str(e)}

async def get_all_students(db):
    try:
        query = "SELECT * FROM Students"
        results = await db.fetch(query)
        students = [dict(result) for result in results]
        for student in students:
            if student.get('DateOfBirth'):
                today = datetime.now().date()
                born = student['DateOfBirth']
                age = today.year - born.year - ((today.month, today.day) < (born.month, born.day))
                student['tuoi'] = age
        return {"data": students, "message": "Lấy danh sách sinh viên thành công"}
    except Exception as e:
        return {"data": None, "message": "Lỗi khi lấy danh sách sinh viên", "error": str(e)}

async def update_student(db, studentId: str, student: Student):
    try:
        date_of_birth = datetime.strptime(student.dateOfBirth, '%Y-%m-%d').date() if student.dateOfBirth else None
        query = """
            UPDATE Students
            SET FullName = $1, DateOfBirth = $2, Gender = $3, Address = $4, Email = $5, Phone = $6, ClassID = $7
            WHERE StudentID = $8
            RETURNING *
        """
        result = await db.fetchrow(
            query,
            student.fullName,
            date_of_birth,
            student.gender,
            student.address,
            student.email,
            student.phone,
            student.classId,
            studentId
        )
        if result:
            return {"message": "Cập nhật sinh viên thành công", "data": dict(result)}
        return {"message": "Cập nhật sinh viên không thành công"}
    except ValidationError as ve:
        return {"message": "Dữ liệu không hợp lệ", "error": str(ve)}
    except Exception as e:
        return {"message": "Cập nhật sinh viên không thành công", "error": str(e)}

async def delete_student(db, studentId: str):
    try:
        query = "DELETE FROM Students WHERE StudentID = $1 RETURNING *"
        result = await db.fetchrow(query, studentId)
        if result is not None:
            return {"message": "Xóa sinh viên thành công", "data": dict(result)}
        return {"message": "Không tìm thấy sinh viên để xóa"}
    except Exception as e:
        return {"message": "Xóa sinh viên không thành công", "error": str(e)}
from typing import List
from fastapi import APIRouter, Depends
from app.students.schemas import StudentScheme, StudentSchemeAdd
from app.students.service import StudentService
from app.students.rb import RBStudent

router = APIRouter(prefix='/students', tags=['Student handler'])

@router.get("/", summary="get all students")
async def get_all_students(request_body: RBStudent = Depends()) -> List[StudentScheme]:
    return await StudentService.find_all_students(**request_body.to_dict())

@router.get("/{id}", summary="get one student by id or none")
async def get_student_by_id(student_id:int) -> StudentScheme | dict:
    result = await StudentService.find_by_id(student_id)
    if result is None:
        return {"message": f"Student with {student_id} not found"}
    return result

@router.post("/add")
async def add_student(student: StudentSchemeAdd) -> dict:
    result = await StudentService.add_student(**student.dict())
    if result:
        return {
            "message": "Added successfully",
            "student": student,
        }
    else:
        return {
            "message": "Error while adding student"
        }

@router.delete("/delete/{id}")
async def delete_student_by_id(student_id: int) -> dict:
    result = await StudentService.delete_student_by_id(student_id)
    if result:
        return {
            "message": "Deleted successfully",
            "student": student_id,
        }
    else:
        return {"message": "Error while deleting student"}
    
    


'''
async def get_student_by_id(student_id:int) -> StudentScheme | dict:
    result = await StudentService.find_one_or_none(student_id)
    if result is None:
        return {"message": f"Student with {student_id} not found"}
    return result    
'''
    
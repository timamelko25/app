from app.majors.models import Major
from app.students.models import Student
from app.service.base import BaseService
from app.database import async_session_maker
from sqlalchemy import delete, insert, select, update, event
from sqlalchemy.orm import joinedload
from sqlalchemy.exc import SQLAlchemyError

class StudentService(BaseService):
    model = Student

    @classmethod
    async def find_by_id(cls, student_id:int):
        async with async_session_maker() as session:
            #first query to get info about student
            query_student = select(cls.model).options(joinedload(cls.model.major)).filter_by(id=student_id)
            result_student = await session.execute(query_student)
            student_info = result_student.scalar_one_or_none()
            
            #if student not found, return none
            if not student_info:
                return None
            
            student_data = student_info.to_dict()
            student_data["major"] = student_info.major.major_name if student_info.major else None
            
            return student_data
    
    @classmethod
    async def find_all_students(cls, **student_data):
        async with async_session_maker() as session:
            query = select(cls.model).options(joinedload(cls.model.major)).filter_by(**student_data)
            result = await session.execute(query)
            student_info = result.scalars().all()
            
            student_data = []
            for student in student_info:
                student_dict = student.to_dict()
                student_dict['major'] = student.major.major_name if student.major else None
                student_data.append(student_dict)
                
            return student_data
    
    '''
    @classmethod
    async def add_student(cls, student_data: dict):
        async with async_session_maker() as session:
            async with session.begin():
                stmt = insert(cls.model).values(**student_data).returning(cls.model.id, cls.model.major_id)
                result = await session.execute(stmt)
                new_student_id, major_id = result.fetchone()

                # Увеличение счетчика студентов в таблице Major
                update_major = (
                    update(Major)
                    .where(Major.id == major_id)
                    .values(count_students=Major.count_students + 1)
                )
                await session.execute(update_major)

                try:
                    await session.commit()
                except SQLAlchemyError as e:
                    await session.rollback()
                    raise e

                return new_student_id
    '''
    @event.listens_for(Student, 'after_insert')
    def receive_after_insert(mapper, connection, target):
        major_id = target.major_id
        connection.execute(
            update(Major)
            .where(Major.id == major_id)
            .values(count_students=Major.count_students + 1)
        )
        
    @classmethod
    async def add_student(cls, **student_data: dict):
        async with async_session_maker() as session:
            async with session.begin():
                new_student = Student(**student_data)
                session.add(new_student)
                await session.flush()
                new_student_id = new_student.id
                await session.commit()
                return new_student_id
            
    @event.listens_for(Student, 'after_delete')
    def receive_after_delete(mapper, connection, target):
        major_id = target.major_id
        connection.execute(
            update(Major)
            .where(Major.id == major_id)
            .values(count_students=Major.count_students - 1)
        )
        
    @classmethod
    async def delete_student_by_id(cls, student_id: int):
        async with async_session_maker() as session:
            async with session.begin():
                query = select(cls.model).filter_by(id=student_id)
                result = await session.execute(query)
                student_to_delete = result.scalar_one_or_none()

                if not student_to_delete:
                    return None

                # Удаляем студента
                await session.execute(
                    delete(cls.model).filter_by(id=student_id)
                )

                await session.commit()
                return student_id
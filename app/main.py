from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.students.router import router as router_students
from app.majors.router import router as router_majors
from app.pages.router import router as router_pages
from app.users.router import router as router_users

'''
from fastapi import FastAPI
from app.utils import dict_list_to_json, json_to_dict_list
import os
from typing import List, Optional
from students.schemas import Student

app = FastAPI()

script_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(script_dir)
path_to_json = os.path.join(parent_dir, 'test.json')

@app.get("/")
async def root():
    return {"message" : "Hello"}

@app.get("/students", response_model = List[Student])
async def get_all_students():
    return json_to_dict_list(path_to_json)

@app.get("/students/{course}")
async def get_all_students_course(course: int):
    students = json_to_dict_list(path_to_json)
    list = []
    for student in students:
        if student["course"] == course:
            list.append(student)
    return list
    
@app.get("/students")
async def get_all_students(course: Optional[int] = None) -> list[Student]:
    students = json_to_dict_list(path_to_json)
    if course is None:
        return students
    else:
        list = []
        for student in students:
            if student["course"] == course:
                list.append(student)
        return list
'''

app = FastAPI()

app.mount('/static', StaticFiles(directory='app/static'), 'static')

@app.get("/", tags=['Root'])
async def get_home():
    return {"message": "Hello"}

app.include_router(router_students)
app.include_router(router_majors)
app.include_router(router_pages)
app.include_router(router_users)
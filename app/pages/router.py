from fastapi import APIRouter, Depends, HTTPException, Request, UploadFile, status
from fastapi.templating import Jinja2Templates
import shutil

from app.students.router import get_all_students, get_student_by_id
from app.users.auth import get_password_hash
from app.users.dependencies import get_current_user
from app.users.models import User
from app.users.router import get_user
from app.users.schemas import UserSchemeReg
from app.users.service import UserService

router = APIRouter(prefix="/pages", tags=["Frontend"])
templates = Jinja2Templates(directory='app/templates')

@router.get('/students')
async def get_students_html(request: Request, students = Depends(get_all_students)):
    return templates.TemplateResponse(
        name='students.html', 
        context={'request': request, 'students': students}
        )

@router.get('/students/{student_id}')
async def get_student_html(request: Request, student = Depends(get_student_by_id)):
    return templates.TemplateResponse(
        name='student.html',
        context={'request': request, 'student': student}
    )

@router.post('/add_photo')
async def add_student_photo(file: UploadFile, image_name:int):
    with open(f'app/static/images/{image_name}.webp', 'wb+') as photo_obj:
        shutil.copyfileobj(file.file, photo_obj)
        
@router.get("/register/")
async def register_user(request: Request) -> dict:
    return templates.TemplateResponse(
        name = 'register.html',
        context={'request': request}
    )

@router.get("/login/")
async def login_user(request: Request) -> dict:
    return templates.TemplateResponse(
        name='login.html',
        context={"request": request}
    )

@router.get("/profile")
async def get_profile(request: Request, profile = Depends(get_user)):
    return templates.TemplateResponse(
        name="profile.html",
        context={"request":request, "profile": profile}
    )
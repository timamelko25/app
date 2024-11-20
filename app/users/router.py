from fastapi import APIRouter, Depends, Response, status, HTTPException
from app.users.auth import create_access_token, get_password_hash, authenticate_user
from app.users.dependencies import get_current_user, get_current_admin_user
from app.users.models import User
from app.users.service import UserService
from app.users.schemas import UserSchemeReg, UserSchemeAuth

router = APIRouter(prefix='/auth', tags=['Authorization'])

@router.post("/register/")
async def register_user(user_data: UserSchemeReg) -> dict:
    user = await UserService.find_one_or_none(email=user_data.email)
    if user:
        raise HTTPException(
            status_code = status.HTTP_409_CONFLICT,
            detail = "User already registered"
        )
    user_dict = user_data.dict()
    user_dict['password'] = get_password_hash(user_data.password)
    await UserService.add(**user_dict)
    return {"message": "Successfully registered"}

@router.post("/login/")
async def auth_user(response: Response, user_data: UserSchemeAuth):
    result = await authenticate_user(email=user_data.email, password = user_data.password)
    if result is None:
        raise HTTPException(
            status_code = status.HTTP_401_UNAUTHORIZED,
            detail="Wrong email or password"
        )
    access_token = create_access_token(
        {"sub": str(result.id)}
    )
    response.set_cookie(key="users_access_token", value=access_token, httponly=True)
    return {
        'access_token': access_token,
        'refresh_token': None
    }
    
@router.get("/user/")
async def get_user(user_data: User = Depends(get_current_user)):
    return user_data

@router.post("/logout/")
async def logout_user(response: Response):
    response.delete_cookie(key="users_access_token")
    return {"message": "User successfully logout"}

@router.get("/all_users")
async def get_all_users(user_data: User = Depends(get_current_admin_user)):
    return await UserService.find_all()
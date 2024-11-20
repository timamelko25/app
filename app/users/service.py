from app.service.base import BaseService
from app.users.models import User


class UserService(BaseService):
    model = User
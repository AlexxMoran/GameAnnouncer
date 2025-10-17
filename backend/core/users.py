from fastapi_users import FastAPIUsers

from models.user import User
from core.deps import get_user_manager
from core.auth import auth_backend


fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend],
)

current_user = fastapi_users.current_user()

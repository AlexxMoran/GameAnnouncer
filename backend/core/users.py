from fastapi_users import FastAPIUsers

from models.user import User
from core.deps import get_user_manager
from core.auth import get_auth_backend, get_refresh_auth_backend


fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [get_auth_backend(), get_refresh_auth_backend()],
)

current_user = fastapi_users.current_user()
current_user_or_none = fastapi_users.current_user(optional=True)

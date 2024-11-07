from typing import Annotated, List

from fastapi import Depends

from app.models.auth_user import User
from ..core.tokens import get_verified_current_user
from ..core.exceptions import UnauthorizedAccess  


class RoleChecker:
    def __init__(self, allowed_roles: List[str]) -> None:
        self.allowed_roles = allowed_roles

    def __call__(self, current_user: Annotated[User, Depends(get_verified_current_user)]) -> bool:
        if current_user.role in self.allowed_roles:
            return True
        
        raise UnauthorizedAccess()
from pydantic import BaseModel


class UserRoleAssignmentCreate(BaseModel):
    role_id: int
    user_id: int

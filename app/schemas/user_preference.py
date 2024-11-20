from pydantic import BaseModel


class UserPreferenceBase(BaseModel):
    preference_type: str
    preference_value: str


class UserPreferenceCreate(UserPreferenceBase):
    user_id: int


class UserPreferenceUpdate(BaseModel):
    preference_type: str
    preference_value: str


class UserPreferenceResponse(UserPreferenceBase):
    class Config:
        orm_mode = True

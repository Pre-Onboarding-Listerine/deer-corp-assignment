from pydantic import BaseModel, Field


class User(BaseModel):
    user_id: int
    name: str = Field(max_length=30)
    password: str

    class Config:
        orm_mode = True

from pydantic import BaseModel, Field
from typing import Optional,List


# Init DaTA 
class InitData(BaseModel):
    data : str

# ПроВерка пользователя 
class UserCheck(BaseModel):
    user_id : int

# Запрос на валидацию 
class AuthInitRequest(BaseModel):
    init_data: str

# Ответ на валидацию 
class AuthInitResponse(BaseModel):
    status: str        
    message: str       
    is_member: bool    

# Описание самого урока 
class LessonShort(BaseModel):
    id: int
    link : str 
    description: str
    cover : str



    class Config:
        orm_mode = True

# Инфо по каждому видео-уроку 
class LessonVideoInfo(BaseModel):
    videoLink: str = Field(..., alias="video_link")
    description: str | None = None
    videoCover: str | None = Field(None, alias="video_cover")

    class Config:
        orm_mode = True
        allow_population_by_field_name = True


# Описание модуля + его список уроков
class ModuleWithLessons(BaseModel):
    id: int
    title: str
    lessons: List[LessonVideoInfo]

    class Config:
        orm_mode = True



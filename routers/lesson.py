from fastapi import APIRouter, Depends, Query, HTTPException, status
from fastapi.exceptions import HTTPException
import os 
from typing import Any, List
from uuid import UUID
from core.auth import check_webapp_signature
from schemas.schemas import UserCheck
from urllib.parse import parse_qsl
from models.models import User, Lesson, CourseModule, Course
from fastapi import Response
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime 
import time 
from sqlalchemy.orm import selectinload
from schemas.schemas import AuthInitRequest, AuthInitResponse, LessonShort, ModuleWithLessons, LessonVideoInfo
from sqlalchemy import select, insert, update, delete
from db.session import get_db
from core.auth import TELEGRAM_BOT_TOKEN, current_user

router = APIRouter()


@router.get("/courses")
async def getListCourses(
    user_data: dict = Depends(current_user), 
    db: AsyncSession = Depends(get_db)
):
    
    result = await db.execute(select(Course))
    courses: List[Course] = result.scalars().all()
    return courses



@router.get("/courses/{id}")
async def getListCourses(
    id : int ,
    user_data: dict = Depends(current_user), 
    db: AsyncSession = Depends(get_db)
):
    
    result = await db.execute(select(Course).where(Course.id == id))
    courses: List[Course] = result.scalars().all()
    return courses


@router.get("/lessons/{course_id}")
async def get_lessons_of_course(
    course_id: int,
    user_data: dict = Depends(current_user),  
    db: AsyncSession = Depends(get_db),
):
    
    result = await db.execute(
    select(CourseModule)
    .where(CourseModule.course_id == course_id)
    .options(selectinload(CourseModule.lessons))
)
    modules: List[CourseModule] = result.scalars().all()

    if not modules:
        raise HTTPException(status_code=404, detail="Курс не найден или у него нет модулей")

    response = []
    for module in modules:
        
        sorted_lessons = sorted(module.lessons, key=lambda l: l.order or 0)

        
        lessons_data = [
            {
                "id": lesson.id,
                "title": lesson.title,
                "duration": int(lesson.duration) if lesson.duration.isdigit() else lesson.duration
            }
            for lesson in sorted_lessons
        ]

        module_data = {
            "id": module.id,
            "title": module.title,
            "lessons": lessons_data
        }
        response.append(module_data)

    return response




@router.get("/{course_id}/{module_id}", response_model=List[LessonVideoInfo])
async def get_lessons_of_module(
    course_id: int,
    module_id: int,
    # user_data: dict = Depends(current_user),  
    db: AsyncSession = Depends(get_db),
):
  
    result = await db.execute(
        select(CourseModule).where(
            CourseModule.id == module_id,
            CourseModule.course_id == course_id
        )
    )
    module = result.scalars().first()
    if not module:
        raise HTTPException(status_code=404, detail="Модуль не найден или не принадлежит этому курсу")

    
    result = await db.execute(
        select(Lesson).where(Lesson.module_id == module_id)
    )

    lessons = result.scalars().all()

    return lessons



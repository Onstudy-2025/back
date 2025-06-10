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




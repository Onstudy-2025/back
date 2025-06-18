from fastapi import APIRouter, Depends, Query, HTTPException, status
from fastapi.exceptions import HTTPException
import os 
from typing import Any, List
from uuid import UUID
from core.auth import check_webapp_signature
from schemas.schemas import UserCheck
from urllib.parse import parse_qsl
from models.models import User, Lesson, CourseModule, Course
from fastapi import Response, Request
import json
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime 
import time 
from sqlalchemy.orm import selectinload
from schemas.schemas import AnswerItem, TestData, CheckAnswers, TestAnswerReturn
from sqlalchemy import select, insert, update, delete
from db.session import get_db
from core.auth import TELEGRAM_BOT_TOKEN, current_user








router = APIRouter()



@router.get("/tests/exactlesson/{lesson_id}")
async def getFullTestWithId(
    lesson_id : int ,
    user_data: dict = Depends(current_user),  
    db: AsyncSession = Depends(get_db)
):  
    base_dir = os.path.dirname(__file__)
    file_path = os.path.join(base_dir, "..", "testlist", f"{lesson_id}.json")

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        raise HTTPException(
            status_code=404,
            detail=f"Тест {lesson_id} не найден"
        )
    
    
   
@router.post("/tests/checktest")
async def getFullTestWithId(
    data : CheckAnswers,
    user_data: dict = Depends(current_user),  
    db: AsyncSession = Depends(get_db)
):
    # Айди самого теста
    test_id = data.data.testId
    # Список ответов 
    answerList = data.data.answers # Ответы пользователя 
    base_dir = os.path.dirname(__file__)
    file_path = os.path.join(base_dir, "..", "testlist", f"{test_id}.json")

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            testdata = json.load(f) # Ответы правильные 
    except FileNotFoundError:
        raise HTTPException(
            status_code=404,
            detail=f"Тест {test_id} не найден"
        )
    questionsCount = 0
    rightAns = 0
    for i in answerList:
        testid = i.questionId
        for j in testdata:
            if j["id"] == testid:
                if j["correctAns"] == i.answerId:
                    rightAns+=1
            else:
                continue

        questionsCount+=1
    

    percentage = (100/questionsCount) * rightAns
    if percentage >= 95:
        grade = "great"
    elif 85<= percentage < 95:
        grade="good"
    elif 75<=percentage< 85:
        grade="fair"
    elif percentage < 75:
        grade="bad"


    return TestAnswerReturn(
        grade=grade,
        correctAnswersCount=rightAns,
        correctAnswersPercent=(100/questionsCount) * rightAns,
        numberOfQuestions=questionsCount
    )
    
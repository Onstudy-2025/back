from fastapi import APIRouter








router = APIRouter()



@router.get("/tests/{lesson_id}")
async def getFullTestWithId(
    lesson_id : int 
):  
    return {"ans" : "True"}
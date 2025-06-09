from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
import uvicorn
from core.config import settings
from routers.router import api_router


app = FastAPI()



app.include_router(api_router)
# Set up CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://frontt-blond.vercel.app","http://localhost:3000"],  # Разрешаем только этот домен
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"],  
)





# Exception handlers
@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request, exc):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail},
    )


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    return JSONResponse(
        status_code=422,
        content={"detail": exc.errors()},
    )


# Health check endpoint
@app.get("/health")
async def health_check():
    return {"status": "healthy"}


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=settings.PROJECT_HOST,
        port=settings.PROJECT_PORT,
        reload=settings.DEBUG,
    )

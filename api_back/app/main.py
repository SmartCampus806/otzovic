from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from starlette.middleware.cors import CORSMiddleware
import logging

from app.routes.api import router as api_router

app = FastAPI(
    title="Otzovik API",
    description="API для отзывов с поддержкой MongoDB",
    version="1.0.0"
)

# CORS (если нужно)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Логирование запросов
logger = logging.getLogger("uvicorn.access")

@app.middleware("http")
async def log_requests(request: Request, call_next):
    logger.info(f"Request: {request.method} {request.url}")
    response = await call_next(request)
    logger.info(f"Response status: {response.status_code}")
    return response

# Подключение роутеров
app.include_router(api_router, prefix="/api")

@app.get("/", tags=["Health"])
async def read_root():
    return {"message": "Welcome to the FastAPI server!"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
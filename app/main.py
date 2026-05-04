from fastapi import FastAPI

from app.api.task_routes import router as task_router

app = FastAPI(
    title="TaskFlow AI",
    description="AI-powered task management API built with FastAPI.",
    version="0.1.0",
)

app.include_router(task_router)


@app.get("/health")
def health_check():
    return {"status": "ok"}

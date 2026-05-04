from fastapi import FastAPI

app = FastAPI(
    title="TaskFlow AI",
    description="AI-powered task management API built with FastAPI.",
    version="0.1.0",
)


@app.get("/health")
def health_check():
    return {"status": "ok"}
"""
Application entry point.
"""

from fastapi import FastAPI

from backend.shared.core.config import settings
from backend.shared.db.mongo import connect_to_mongo, close_mongo_connection

# Routers
from backend.admin.users.routes import router as users_router
from backend.admin.auth.routes import router as auth_router
from backend.shared.routes import protected

# Tasks
from backend.shared.tasks.sample_tasks import long_running_task


# -----------------------------
# Create FastAPI application
# -----------------------------
app = FastAPI(title=settings.APP_NAME)


# -----------------------------
# Startup / Shutdown events
# -----------------------------
@app.on_event("startup")
def startup():
    connect_to_mongo()


@app.on_event("shutdown")
def shutdown():
    close_mongo_connection()


# -----------------------------
# Register Routers
# -----------------------------
app.include_router(auth_router)
app.include_router(users_router)
app.include_router(protected.router)


# -----------------------------
# Basic Routes
# -----------------------------
@app.get("/")
def root():
    return {"message": "Backend is running successfully"}


@app.get("/health")
def health_check():
    return {"status": "healthy"}


# -----------------------------
# Celery Test Route
# -----------------------------
@app.post("/test-task")
def trigger_task(data: str):
    task = long_running_task.delay(data)
    return {"task_id": task.id}

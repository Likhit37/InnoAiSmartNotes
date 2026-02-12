"""
Celery Application Configuration

Initializes the Celery worker instance and explicitly
registers all task modules to avoid discovery issues.
"""

from celery import Celery

# Redis broker URL (must match docker service name)
REDIS_URL = "redis://redis:6379/0"

# Create Celery instance
celery = Celery(
    "innosmart_worker",
    broker=REDIS_URL,
    backend=REDIS_URL,
)

# Explicitly import task modules to ensure registration
import backend.shared.tasks.sample_tasks  # noqa: F401

# Celery configuration
celery.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="Asia/Kolkata",
    enable_utc=True,
)

"""
Sample Celery task for testing async processing.
"""

from backend.shared.tasks.celery_app import celery
import time


@celery.task(name="backend.shared.tasks.sample_tasks.long_running_task")
def long_running_task(data: str):
    """
    Simulates a long-running task.
    """
    print(f"[Worker] Task started with data: {data}")
    time.sleep(5)
    print("[Worker] Task completed")

    return {
        "status": "completed",
        "data": data
    }

# # celery_config.py
from celery import Celery

app = Celery(
    "tasks",
    broker="redis://localhost:6379/0",  # Redis as broker
    backend="redis://localhost:6379/0",
    include=['tasks']  # This line registers the tasks module
)

# Configure Celery
app.conf.update(
    # Worker settings
    worker_pool='solo',  # Use solo pool to reduce memory usage
    worker_concurrency=1,  # Only one worker process
    worker_max_tasks_per_child=1,  # Restart worker after each task
    worker_max_memory_per_child=150000,  # 150MB memory limit per worker
    
    # Task settings
    task_time_limit=300,  # 5 minutes
    task_soft_time_limit=240,  # 4 minutes
    
    # Beat schedule
    beat_schedule={
        "scrape-every-3-days": {
            "task": "tasks.scrape_major_categories",
            "schedule": 259200,  # Every 3 days (60 * 60 * 24 * 3 seconds)
        },
    },
    timezone="UTC"
)



# from celery import Celery
# import os

# app = Celery(
#     "tasks",
#     broker=os.getenv("CELERY_BROKER_URL", "redis://localhost:6379/0"),
#     backend=os.getenv("CELERY_RESULT_BACKEND", "redis://localhost:6379/0"),
#     include=['tasks']
# )

# app.conf.update(
#     worker_pool='solo',
#     worker_concurrency=1,
#     worker_max_tasks_per_child=1,
#     worker_max_memory_per_child=150000,
#     task_time_limit=300,
#     task_soft_time_limit=240,
#     beat_schedule={
#         "scrape-every-3-days": {
#             "task": "tasks.scrape_major_categories",
#             "schedule": 259200,
#         },
#         "scrape-reviews-daily": {
#             "task": "tasks.scrape_product_reviews_task",
#             "schedule": 86400,
#         },
#         "compute-recommendations-daily": {
#             "task": "tasks.compute_recommendations",
#             "schedule": 86400,
#         },
#     },
#     timezone="UTC"
# )
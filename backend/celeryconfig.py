from app.config import settings

broker_url = settings.broker_url

worker_redirect_stdouts = False

task_serializer = "json"
result_serializer = "json"
accept_content = ["json"]
timezone = "UTC"
enable_utc = True

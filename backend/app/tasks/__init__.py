from celery import Celery

celery_app = Celery("worker")
celery_app.config_from_object("celeryconfig")

# lazy import:
to_import = [("app.tasks.account", "list_account_products_task")]

for module, task in to_import:
    module = __import__(module, fromlist=[task])
    celery_app.register_task(getattr(module, task))
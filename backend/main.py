from app.prisma import shutdown, startup
from app.routers import account, download, log, platform, setting
from fastapi import FastAPI

app = FastAPI()

app.include_router(download.router, prefix="/download", tags=["download"])
app.include_router(account.router, prefix="/account", tags=["account"])
app.include_router(log.router, prefix="/log", tags=["log"])
app.include_router(setting.router, prefix="/setting", tags=["setting"])
app.include_router(platform.router, prefix="/platform", tags=["platform"])

app.add_event_handler("startup", startup)
app.add_event_handler("shutdown", shutdown)


@app.get("")
def read_root():
    return {"message": "Welcome to CoursesDownloader Backend"}

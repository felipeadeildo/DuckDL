from app.routers import account, download
from fastapi import FastAPI

app = FastAPI()

app.include_router(download.router, prefix="/download")
app.include_router(account.router, prefix="/account")


@app.get("/")
def read_root():
    return {"message": "Welcome to CoursesDownloader Backend"}

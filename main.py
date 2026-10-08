from fastapi import FastAPI
from routers import auth, users, tasks

app = FastAPI()

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(tasks.router)


@app.get("/")
def home():
    return {"message": "This is Backend"}
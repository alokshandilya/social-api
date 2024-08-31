from fastapi import FastAPI

from app.routers import auth, post, user, vote

app = FastAPI()


@app.get("/")
def read_root():
    return {"data": "Hello World"}


app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)

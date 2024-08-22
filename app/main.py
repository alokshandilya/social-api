from typing import List

from dotenv import load_dotenv
from fastapi import Depends, FastAPI, HTTPException, Response, status
from sqlalchemy.orm import Session

from . import models, schemas, utils
from .database import engine, get_db

load_dotenv()

app = FastAPI()

models.Base.metadata.create_all(bind=engine)


@app.get("/")
def read_root():
    return {"data": "Hello World"}


@app.get("/posts", response_model=List[schemas.Post])
def read_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return posts


@app.post(
    "/posts",
    status_code=status.HTTP_201_CREATED,
    response_model=schemas.Post,
)
def create_post(post: schemas.PostBase, db: Session = Depends(get_db)):
    new_post = models.Post(**post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)  # refresh the object to get the id
    return new_post


@app.get("/posts/{id}", response_model=schemas.Post)
def get_post(id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id: {id} was not found",
        )
    return post


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db)):
    post_query = db.query(models.Post).filter(models.Post.id == id)

    if post_query.first() is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id: {id} was not found",
        )
    post_query.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{id}", response_model=schemas.Post)
def update_post(
    id: int,
    updated_post: schemas.PostCreate,
    db: Session = Depends(get_db),
):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()

    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id: {id} was not found",
        )
    post_query.update(updated_post.model_dump(), synchronize_session=False)
    db.commit()
    return post_query.first()


@app.post(
    "/users",
    status_code=status.HTTP_201_CREATED,
    response_model=schemas.UserOut,
)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    # hash the password - user.password
    hashed_password = utils.hash(user.password)
    user.password = hashed_password

    new_user = models.User(**user.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@app.get("/users/{id}", response_model=schemas.UserOut)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"user with id: {id} was not found",
        )
    return user

import os
import time
from random import randrange

import psycopg2
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Response, status
from psycopg2.extras import RealDictCursor
from pydantic import BaseModel

load_dotenv()

app = FastAPI()


class Post(BaseModel):
    title: str
    content: str
    published: bool = True


while True:
    try:
        conn = psycopg2.connect(
            host=os.getenv("host"),
            database=os.getenv("database"),
            user=os.getenv("user"),
            password=os.getenv("password"),
            cursor_factory=RealDictCursor,
        )
        cursor = conn.cursor()
        print("Connected to the database")
        break
    except Exception as e:
        print("I am unable to connect to the database")
        print(f"error: {e}")
        time.sleep(5)


my_posts = [
    {"title": "Post 1", "content": "This is the content of post 1", "id": 1},
    {"title": "Post 2", "content": "This is the content of post 2", "id": 2},
]


def find_posts(id: int):
    for post in my_posts:
        if post["id"] == id:
            return post
    return None


@app.get("/")
def read_root():
    return {"data": "Hello World"}


@app.get("/posts")
def read_posts():
    cursor.execute("""SELECT * FROM posts""")
    posts = cursor.fetchall()
    return {"data": posts}


@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(post: Post):
    post_dict = post.model_dump()
    post_dict["id"] = randrange(0, 1000000)
    my_posts.append(post_dict)
    return {"data": "Post created successfully"}


@app.get("/posts/{id}")
def get_post(id: int):
    cursor.execute("""SELECT * FROM posts WHERE id = %s""", (id,))
    post = cursor.fetchone()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id: {id} was not found",
        )
    return {"post_detail": post}


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    post = find_posts(id)
    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id: {id} was not found",
        )
    my_posts.remove(post)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    existing_post = find_posts(id)
    if existing_post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id: {id} was not found",
        )
    existing_post_index = my_posts.index(existing_post)
    updated_post = post.model_dump()
    updated_post["id"] = id
    my_posts[existing_post_index] = updated_post
    return {"data": "Post updated successfully"}

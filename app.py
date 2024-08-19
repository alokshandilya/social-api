from random import randrange
from typing import Optional

from fastapi import FastAPI, HTTPException, Response, status
from pydantic import BaseModel

app = FastAPI()


class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None


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
    return {"data": my_posts}


@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(post: Post):
    post_dict = post.model_dump()
    post_dict["id"] = randrange(0, 1000000)
    my_posts.append(post_dict)
    return {"data": "Post created successfully"}


@app.get("/posts/{id}")
def get_post(id: int):
    post = find_posts(id)
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

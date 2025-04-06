from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
from uuid import uuid4
app = FastAPI()


class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None
    id: str = uuid4()


db = [
    {"title": "Living in Lagos: A Survival Guide",
        "content": "Lagos is a bustling city with a lot to offer, but it can be overwhelming for newcomers. Here are some tips to help you navigate the city.", "rating": 5, "id": uuid4()},
    {"title": "The Best Places to Eat in Lagos",
        "content": "Lagos is a foodie's paradise, with a wide range of restaurants and street food vendors. Here are some of the best places to eat in the city.", "rating": 5, "id": uuid4()}
]


def find_post(id):
    for post in db:
        if str(post['id']) == str(id):  # Convert both to strings for comparison
            return post
    return None


@app.get("/")
def read_root():
    return {"message": "Hello, Godswill!"}


@app.get("/posts")
def get_posts():
    return {"data": db}


@app.get("/posts/{id}")  # path parameter
def get_post(id: str, response: Response):
    post = find_post(id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} not found")
    return post


@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(payload: Post):
    payload_dict = payload.model_dump()
    payload_dict['rating'] = 5
    db.append(payload_dict)
    return {"message": "successfully created post", "data": payload_dict}


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: str):
    post = find_post(id)
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} not found")
    db.remove(post)
    return None


@app.put("/posts/{id}")
def update_post(id: str, payload: Post):
    post = find_post(id)
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} not found")

    post_index = db.index(post)
    db[post_index].update(payload.model_dump(exclude_unset=True))

    return {"message": "successfully updated post", "data": db[post_index]}

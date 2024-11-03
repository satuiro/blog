from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
import models, schemas, auth
from database import get_db

app = FastAPI()

# Include auth router
app.include_router(auth.router)


@app.get("/")
def read_root():
    return {"message": "Welcome to BLOG API"}


@app.post("/blogs/", response_model=schemas.Blog)
def create_blog(
    blog: schemas.BlogCreate,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(auth.get_current_user),
):
    db_blog = models.Blog(**blog.dict(), author_id=current_user.id)
    db.add(db_blog)
    db.commit()
    db.refresh(db_blog)
    return db_blog


@app.get("/blogs/", response_model=List[schemas.Blog])
def read_blogs(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    blogs = db.query(models.Blog).offset(skip).limit(limit).all()
    return blogs


@app.get("/blogs/{blog_id}", response_model=schemas.Blog)
def read_blog(blog_id: int, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == blog_id).first()
    if blog is None:
        raise HTTPException(status_code=404, detail="Blog not found")
    return blog


@app.put("/blogs/{blog_id}", response_model=schemas.Blog)
def update_blog(
    blog_id: int,
    blog: schemas.BlogCreate,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(auth.get_current_user),
):
    db_blog = db.query(models.Blog).filter(models.Blog.id == blog_id).first()
    if db_blog is None:
        raise HTTPException(status_code=404, detail="Blog not found")
    if db_blog.author_id != current_user.id:
        raise HTTPException(
            status_code=403, detail="Not authorized to update this blog"
        )

    for var, value in blog.dict().items():
        setattr(db_blog, var, value)

    db.commit()
    db.refresh(db_blog)
    return db_blog


@app.delete("/blogs/{blog_id}")
def delete_blog(
    blog_id: int,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(auth.get_current_user),
):
    blog = db.query(models.Blog).filter(models.Blog.id == blog_id).first()
    if blog is None:
        raise HTTPException(status_code=404, detail="Blog not found")
    if blog.author_id != current_user.id:
        raise HTTPException(
            status_code=403, detail="Not authorized to delete this blog"
        )

    db.delete(blog)
    db.commit()
    return {"message": "Blog deleted successfully"}


@app.post("/blogs/{blog_id}/comments/", response_model=schemas.Comment)
def create_comment(
    blog_id: int,
    comment: schemas.CommentCreate,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(auth.get_current_user),
):
    blog = db.query(models.Blog).filter(models.Blog.id == blog_id).first()
    if not blog:
        raise HTTPException(status_code=404, detail="Blog not found")

    db_comment = models.Comment(
        **comment.dict(), blog_id=blog_id, author_id=current_user.id
    )
    db.add(db_comment)
    db.commit()
    db.refresh(db_comment)
    return db_comment


@app.put("/blogs/{blog_id}/like")
def like_blog(
    blog_id: int,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(auth.get_current_user),
):
    blog = db.query(models.Blog).filter(models.Blog.id == blog_id).first()
    if not blog:
        raise HTTPException(status_code=404, detail="Blog not found")

    # Check if user already liked the blog
    like = (
        db.query(models.Like)
        .filter(models.Like.blog_id == blog_id, models.Like.user_id == current_user.id)
        .first()
    )

    if like:
        # Unlike if already liked
        db.delete(like)
        blog.likes_count -= 1
    else:
        # Add new like
        new_like = models.Like(blog_id=blog_id, user_id=current_user.id)
        db.add(new_like)
        blog.likes_count += 1

    db.commit()
    return {"likes_count": blog.likes_count}

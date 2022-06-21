import datetime as _dt
import secrets
from typing import Optional, List
from fastapi import APIRouter, HTTPException, status, Request, Form, UploadFile, File

from PIL import Image
from pydantic import ValidationError

from services.g2tservices import Manager

from schemas.firebasemodels import Message
from schemas.post_schema import PostIn, PostOut
from schemas.comment_schema import CommentIn


router = APIRouter(
    prefix="/post",
    tags=["Post"]
)


async def process_image(img, req) -> str:
    MEDIA_DIR = "./static/media/"
    media_types = ['jpeg', 'png', 'jpg']

    file_name = img.filename

    extension = file_name.split(".")[1]

    if extension not in media_types:
        raise HTTPException(status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
                            detail="File extension not allowed.  Allowed extensions are jpg, jpeg and png")

    image_token_name = secrets.token_hex(10) + "." + extension
    generated_image_name = MEDIA_DIR + image_token_name
    image_content = await img.read()

    with open(generated_image_name, "wb") as url:
        url.write(image_content)
        # shutil.copyfileobj(image.file, url)

    url = str(f"{req.base_url}{generated_image_name[2:]}")

    image = Image.open(generated_image_name)
    image = image.resize(size=(600, 600))
    image.save(generated_image_name)

    img.close()
    return url


@router.post('', status_code=status.HTTP_201_CREATED)
async def create_post(
    request: Request,
    name: str = Form(...),
    body: str = Form(...),
    image: UploadFile = File(...),
    user_id: str = Form(...)
): # changed
    """Create a new post"""

    url = await process_image(img=image, req=request)

    post = PostIn(name=name, body=body, image=url, user_id=user_id)

    date_created = _dt.datetime.timestamp(_dt.datetime.utcnow())
    new_post = {**post.dict(), "date": date_created}
    create_post = Manager().create(collection='post', data_obj=new_post)
    
    return create_post


@router.get('/all/', response_model=List[PostOut])
async def fetch_all_posts(): # changed
    """Fetch all posts"""
    posts = Manager().get_all(collection='post')
    if not posts:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="No job posts available. Create some and try again.")
    return posts

@router.put('/{post_id}/') # => remember, include the response model
async def update_post(post_id: str,
                      request: Request,
                      name: Optional[str] = Form(None),
                      body: Optional[str] = Form(None),
                      image: Optional[UploadFile] = File(None),
                      user_id: Optional[str] = Form(None)):
    """Update a post that corresponds to the provided post id"""
    old_data = Manager().get_one(collection='post', uid=post_id)[0]
    if not old_data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Post not found. Check the post id and try again.")

    url = await process_image(img=image, req=request) if image else old_data.get('image')

    new_name = name if name else old_data.get('name')
    new_body = body if body else old_data.get('body')
    new_user_id = user_id if user_id else old_data.get('user_id')

    try:
        post_body = PostIn(name=new_name, body=new_body, image=url, user_id=new_user_id)
    except ValidationError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Bad request")

    Manager().update(collection='post', uid=post_id, data_obj=post_body.dict())

    return Message(message="Successfully updated the record")


@router.delete('/del/{post_id}/', response_model=Message)
async def delete_post(post_id: str):
    """Delete post that corresponds to the provided post id"""
    deleted_post = Manager().delete(collection='post', uid=post_id)
    if not deleted_post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Post not found. Check the post id and try again.")
    return Message(message="Successfully Deleted")


@router.post('/comment/{post_id}/{user_id}', response_model=Message)
async def create_comment_post(post_id: str, user_id: str, comment: CommentIn): # changed
    """Create a comment for a post if it exists. A user id for the user creating the post is also required"""
    date_created = _dt.datetime.timestamp(_dt.datetime.utcnow())

    is_valid = Manager().validate(collection="post", document=post_id)
    if is_valid:
        new_comment = {**comment.dict(), "date": date_created, "user_id": user_id}

        is_updated = Manager().create_comments(collection='post', uid=post_id, comment_obj=new_comment)
        return Message(message="Comment was created successfully")
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Post not found. Check the post id and try again.")


@router.get('/like/{post_id}/{user_id}', response_model=Message)
async def like_post(post_id: str, user_id: str): # changed
    """Like or dislike a post. user_id is required"""
    is_valid = Manager().validate(collection='post', document=post_id)
    if is_valid:
        Manager().like_unlike(collection='post', uid=user_id, post_id=post_id)
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Post not found. Check the post id and try again.")

    return Message(message="Success")

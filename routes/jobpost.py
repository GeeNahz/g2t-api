import datetime as _dt
import shutil
import secrets
from typing import Optional, List
from PIL import Image
from fastapi import APIRouter, HTTPException, status, File, UploadFile, Form, Request
from pydantic import ValidationError

from services.g2tservices import Manager

from schemas.firebasemodels import CommentIn, CommentOut, JobOut, Message, JobIn


router = APIRouter(
    prefix="/job",
    tags=["Job Post"]
)

"""
job title
company name
job post url
job location
job description
"""


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

    await img.close()
    return url


@router.post('/jobpost/', response_model=JobOut)
async def create_job(request: Request,
                     position: str = Form(...), salary: str = Form(...),
                     title: str = Form(...), job_description: str = Form(...),
                     requirements: str = Form(...), company_name: str = Form(...),
                     location: str = Form(...), job_type: str = Form(...),
                     link: str = Form(...), image: UploadFile = File(...)):

    url = await process_image(img=image, req=request)
    try:
        new_job = JobIn(
            position=position,
            salary=salary, title=title, job_description=job_description,
            requirements=requirements, company_name=company_name,
            location=location, image=url, job_type=job_type, link=link
        )
    except ValidationError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Bad request")

    date_created = _dt.datetime.timestamp(_dt.datetime.utcnow())

    job = {**new_job.dict(), "date":date_created}
    
    return Manager().create(collection='jobpost', data_obj=job)


@router.get('/all/', response_model=List[JobOut])
async def fetch_all_job_posts():
    job_posts = Manager().get_all(collection='jobpost')
    if not job_posts:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="No job posts available. Create some and try again.")
    return job_posts

# Updated
@router.put('/post/{post_id}/', response_model=Message)
async def update_job_post(
    post_id: str,
    request: Request,
    position: Optional[str] = Form(None), salary: Optional[str] = Form(None), title: Optional[str] = Form(None), job_description: Optional[str] = Form(None), requirements: Optional[str] = Form(None), company_name: Optional[str] = Form(None), location: Optional[str] = Form(None), job_type: Optional[str] = Form(None), link: Optional[str] = Form(None), image: Optional[UploadFile] = File(None),
    ):

    """
    Updates a job post that corresponds to the job post id provided
    """

    old_post = Manager().get_one(collection='jobpost', uid=post_id)[0]

    if not old_post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Job post not found. Check the id and try again.")

    new_url = await process_image(img=image, req=request) if image else old_post.get('image')

    new_position = position if position else old_post.get('position')
    new_salary = salary if salary else old_post.get('salary')
    new_title = title if title else old_post.get('title')
    new_job_description = job_description if job_description else old_post.get(
        'job_description')
    new_requirements = requirements if requirements else old_post.get(
        'requirements')
    new_company_name = company_name if company_name else old_post.get(
        'company_name')
    new_location = location if location else old_post.get('location')
    new_job_type = job_type if job_type else old_post.get('job_type')
    new_link = link if link else old_post.get('link')

    try:
        job_update = JobIn(position=new_position, salary=new_salary, title=new_title, job_description=new_job_description, requirements=new_requirements,location=new_location, image=new_url, company_name=new_company_name, job_type=new_job_type, link=new_link)
    except ValidationError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Bad request")

    Manager().update(collection='jobpost', uid=post_id, data_obj=job_update.dict())
    return Message(message="Successfully updated the record.")


@router.post('/comment/{post_id}/{user_id}', response_model=CommentOut)
async def create_comment_post(post_id: str, user_id: str, comment: CommentIn):
    """
    Create a comment for a job post
    """
    date_created = _dt.datetime.timestamp(_dt.datetime.utcnow())

    is_valid = Manager().validate(collection='jobpost', document=post_id)
    if is_valid:
        new_comment = {**comment.dict(), "date": date_created,
                       "user_id": user_id}
        is_updated = Manager().create_comments(collection='jobpost', uid=post_id, comment_obj=new_comment)
        return is_updated
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Job post not found. Check the id and try again.")


@router.get('/like/{post_id}/{uuid}', response_model=Message)
async def like_unlike_post(post_id: str, uuid: str):  # changed
    """
    Like a post if the user id is not in the likes array otherwise unlike the post
    """

    found = Manager().like_unlike(collection='jobpost', uid=uuid, post_id=post_id)
    if not found:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Post not found. Check the post id and try again.")
    return Message(message="Success")

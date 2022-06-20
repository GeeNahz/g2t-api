import datetime as _dt
from typing import List
from fastapi import APIRouter, HTTPException, status

from schemas.firebasemodels import ContactIn, ContactOut

from services.g2tservices import Manager


router = APIRouter(
    prefix="/contact",
    tags=["Contact Details"]
)


@router.post('/')
async def create_contact(contact: ContactIn):
    date_posted = _dt.datetime.timestamp(_dt.datetime.utcnow())
    date_updated = _dt.datetime.timestamp(_dt.datetime.utcnow())

    new_contact = {**contact.dict(), "date_posted": date_posted, "date_updated": date_updated}
    posted = Manager().create(collection='contact', data_obj=new_contact)
    return posted


@router.get('/all/', response_model=List[ContactOut])
async def fetch_all_contacts():
    contacts = Manager().get_all(collection='contact')
    if not contacts:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="No job posts available. Create some and try again.")
    return contacts

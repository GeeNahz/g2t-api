import datetime as _dt
from typing import List
from fastapi import APIRouter, HTTPException, status

from schemas.contact_schema import ContactIn, ContactOut

from services.g2tservices import Manager


router = APIRouter(
    prefix="/contact",
    tags=["Contact Details"]
)


@router.post('/')
async def create_contact(contact: ContactIn):
    """Create a ne contact info"""
    date_posted = _dt.datetime.timestamp(_dt.datetime.utcnow())

    new_contact = {**contact.dict(), "date_posted": date_posted}
    posted = Manager().create(collection='contact', data_obj=new_contact)
    return posted


@router.get('/all/', response_model=List[ContactOut])
async def fetch_all_contacts():
    """Fetch all contacts info"""
    contacts = Manager().get_all(collection='contact')
    if not contacts:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="No job posts available. Create some and try again.")
    return contacts

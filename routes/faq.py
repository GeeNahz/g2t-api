import datetime as _dt
from typing import List
from fastapi import APIRouter, HTTPException, status

from services.g2tservices import Manager

from schemas.faq_schema import Faq


router = APIRouter(
    prefix="/faq",
    tags=["FAQs"]
)


@router.post('/create',)
async def create_faq(faq: Faq):
    """Create a new FAQ"""
    posted = Manager().create(collection='faq', data_obj=faq.dict())
    return posted


@router.get('/all/', response_model=List[Faq])
async def fetch_all_faqs():
    """Fetch all FAQs"""
    faqs = Manager().get_all(collection='faq')
    if not faqs:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="No job posts available. Create some and try again.")
    return faqs

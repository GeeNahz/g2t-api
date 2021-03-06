from fastapi import APIRouter, HTTPException, status

from services.g2tservices import Manager

from schemas.user_schema import User, Finduser


router = APIRouter(
    prefix="/user",
    tags=["User Details"]
)


@router.get('/profiles/{p_user}/{r_user}')
async def get_profile_and_record(p_uuid: str, r_uuid: str):
    """This may not work because either profile or record collection is not available

    Receives user id for profile as p_uuid and user id for record as r_uuid then returns their data
    """
    
    is_valid_profile = Manager().validate(collection='profiles', document=p_uuid)
    if is_valid_profile:
        user_profile = Manager().get_one(collection='profiles', uid=p_uuid)
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="User profile not found. Check the user and try again.")
    
    is_valid_record = Manager().validate(collection='record', document=r_uuid)
    if is_valid_record:
        user_record = Manager().get_one(collection='record', uid=r_uuid)
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="User record not found. Check the user and try again.")

    return {
        "profile": user_profile,
        "record": user_record
    }


@router.get('/getusers/{db_filter}/{query}')
async def filter_items(query: str, db_filter: str):
    """db_filter -> what field to search from
    query -> what value to search for"""

    some_obj = Manager().filter_db(collection='profiles', **{db_filter:query}) 
    if (not some_obj) or (len(some_obj) < 1):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No record matches the query strings")
    else:
        return some_obj


@router.get('/profiles')
async def get_profiles():
    """A test endpoint"""
    profiles = Manager().get_all(collection='profiles')
    if not profiles:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No profile data found")
    else:
        return profiles

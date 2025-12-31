from .data import CONTACT_DETAILS

async def get_college_contact_details():
    try:
        return CONTACT_DETAILS
    except:
        return {'status':'Error occure while fetching other scholarships information'}


